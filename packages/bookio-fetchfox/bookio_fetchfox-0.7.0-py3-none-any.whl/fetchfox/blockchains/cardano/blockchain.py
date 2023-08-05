import logging
from datetime import datetime
from functools import lru_cache
from typing import Iterable

import pytz

from fetchfox.apis import bookio
from fetchfox.apis.cardano import blockfrostio, cnfttools, handleme, jpgstore
from fetchfox.blockchains.base import Blockchain
from fetchfox.constants.blockchains import CARDANO
from fetchfox.constants.currencies import ADA
from fetchfox.constants.marketplaces import JPG_STORE
from fetchfox.dtos import (
    AssetDTO,
    CampaignDTO,
    FloorDTO,
    HoldingDTO,
    ListingDTO,
    RankDTO,
    SaleDTO,
    SaleType,
)
from fetchfox.helpers import formatters
from . import utils

WINTER_NFT_ADDRESS = "addr1qxnrv2quqxhvwxtxmygsmkufph4kjju6j5len7k2ljslpz8ql7k7gehlfvj6ektgu9ns8yx8epcp66337khxeq82rpgqe6lqyk"

logger = logging.getLogger(__name__)


class Cardano(Blockchain):
    def __init__(self, blockfrostio_project_id: str = None):
        super().__init__(
            name=CARDANO,
            currency=ADA,
            logo="https://s2.coinmarketcap.com/static/img/coins/64x64/2010.png",
        )

        self.blockfrostio_project_id: str = blockfrostio_project_id

    def check_collection_id(self, collection_id: str):
        if not utils.is_policy_id(collection_id):
            raise ValueError(f"{collection_id} is not a valid cardano policy id")

    def check_asset_id(self, asset_id: str):
        if not utils.is_asset_id(asset_id):
            raise ValueError(f"{asset_id} is not a valid cardano asset id")

    def check_wallet(self, wallet: str):
        if not utils.is_wallet(wallet):
            raise ValueError(f"{wallet} is not a valid cardano address, stake key or ada handle")

    def explorer_url(self, collection_id: str) -> str:
        return f"https://cardanoscan.io/tokenPolicy/{collection_id}"

    def marketplace_url(self, collection_id: str) -> str:
        return f"https://www.jpg.store/collection/{collection_id}"

    @lru_cache
    def get_stake_key(self, wallet: str) -> str:
        self.check_wallet(wallet)

        if utils.is_stake_key(wallet):
            return wallet

        if utils.is_address(wallet):
            return blockfrostio.get_stake_address(
                wallet,
                project_id=self.blockfrostio_project_id,
            )

        if utils.is_ada_handle(wallet):
            return handleme.resolve_handle(wallet)

        return None

    def get_assets(self, collection_id: str, discriminator: str = None, fetch_metadata: bool = True, *args, **kwargs) -> Iterable[AssetDTO]:
        self.check_collection_id(collection_id)

        response = blockfrostio.get_assets(
            collection_id,
            project_id=self.blockfrostio_project_id,
        )

        for asset_id in response:
            policy_id, asset_name = utils.split_asset_id(asset_id)

            # required for multi-book policies (e.g. monsters, greek classics)
            if discriminator:
                if discriminator not in asset_name.lower():
                    continue

            if fetch_metadata:
                yield self.get_asset(
                    collection_id=collection_id,
                    asset_id=asset_id,
                )
            else:
                yield AssetDTO(
                    collection_id=collection_id,
                    asset_id=asset_id,
                    metadata={},
                )

    def get_asset(self, collection_id: str, asset_id: str, *args, **kwargs) -> AssetDTO:
        self.check_collection_id(collection_id)
        self.check_asset_id(asset_id)

        response = blockfrostio.get_asset_data(
            asset_id,
            project_id=self.blockfrostio_project_id,
        )

        metadata = response.get("onchain_metadata", {})

        return AssetDTO(
            collection_id=collection_id,
            asset_id=asset_id,
            metadata=metadata,
        )

    def get_campaigns(self) -> Iterable[CampaignDTO]:
        for campaign in bookio.campaigns():
            if campaign["blockchain"] != CARDANO:
                continue

            landing = campaign["landing"]
            pricing = landing["price_description"].replace(" (+2 ADA that will be returned with your eBook)", "").strip()

            collection_id = landing["lottery"]["collection_id"]
            start_at = campaign["start_at"]

            yield CampaignDTO(
                blockchain=CARDANO,
                parlamint_id=campaign["id"],
                collection_id=collection_id,
                name=campaign["display_name"],
                description=campaign["landing"]["opener"],
                price=landing["price"],
                supply=campaign["total_deas"],
                pricing=pricing,
                limit=campaign["max_quantity"],
                start_at=formatters.timestamp(start_at["start_at"]),
                explorer_url=f"https://pool.pm/nfts/{collection_id}",
                marketplace_url=self.marketplace_url(collection_id),
                rarity_chart_url=landing["rarity_chart_url"],
            )

    def get_holdings(self, wallet: str, *args, **kwargs) -> Iterable[HoldingDTO]:
        self.check_wallet(wallet)

        stake_address = self.get_stake_key(wallet)

        holdings = blockfrostio.get_holdings(
            stake_address,
            project_id=self.blockfrostio_project_id,
        )

        for holding in holdings:
            asset_id = holding["unit"]

            if asset_id == "lovelace":
                continue

            quantity = int(holding["quantity"])

            policy_id, _ = utils.split_asset_id(asset_id)

            yield HoldingDTO(
                collection_id=policy_id,
                asset_id=asset_id,
                address=stake_address,
                quantity=quantity,
            )

    def get_ranks(self, collection_id: str, *args, **kwargs) -> Iterable[RankDTO]:
        self.check_collection_id(collection_id)

        for asset_name, rank in cnfttools.get_ranks(collection_id).items():
            number = int("".join((c for c in asset_name if c.isdigit())))

            yield RankDTO(
                collection_id=collection_id,
                number=number,
                asset_id=None,
                rank=int(rank),
            )

    def get_rank(self, collection_id: str, asset_id: str, *args, **kwargs) -> RankDTO:
        self.check_collection_id(collection_id)
        self.check_asset_id(asset_id)

        _, asset_name = utils.split_asset_id(asset_id)
        number = int("".join((c for c in asset_name if c.isdigit())))

        rank = cnfttools.get_rank(asset_id)

        return RankDTO(
            collection_id=collection_id,
            asset_id=asset_id.lower(),
            number=number,
            rank=int(rank),
        )

    def get_snapshot(self, collection_id: str, discriminator: str = None, *args, **kwargs) -> Iterable[HoldingDTO]:
        self.check_collection_id(collection_id)

        for asset in self.get_assets(collection_id, discriminator=discriminator, fetch_metadata=False):
            holding = blockfrostio.get_owner(
                asset.asset_id,
                project_id=self.blockfrostio_project_id,
            )

            stake_address = self.get_stake_key(holding["address"])

            yield HoldingDTO(
                collection_id=collection_id,
                asset_id=holding["asset_id"],
                address=stake_address,
                quantity=holding["amount"],
            )

    def get_listings(self, collection_id: str, discriminator: str = None, *args, **kwargs) -> Iterable[ListingDTO]:
        self.check_collection_id(collection_id)

        if discriminator:
            discriminator = discriminator.lower()

        for listing in jpgstore.get_listings(collection_id):
            asset_id = listing["asset_id"]
            policy_id, asset_name = utils.split_asset_id(asset_id)

            # required for multi-book policies (e.g. monsters, greek classics)
            if discriminator:
                if discriminator not in asset_name.lower():
                    continue

            asset_ids = []
            asset_names = []

            if listing["listing_type"] == "BUNDLE":
                for bundled_asset in listing["bundled_assets"]:
                    asset_ids.append(bundled_asset["asset_id"])
                    asset_names.append(bundled_asset["display_name"])
            else:
                asset_ids.append(listing["asset_id"])
                asset_names.append(listing["display_name"])

            if listing.get("confirmed_at"):
                listed_at = datetime.fromisoformat(listing["confirmed_at"].replace("Z", "+00:00"))
            else:
                listed_at = datetime.now(tz=pytz.utc)

            yield ListingDTO(
                identifier=listing["tx_hash"],
                collection_id=policy_id,
                asset_ids=asset_ids,
                asset_names=asset_names,
                listing_id=listing["listing_id"],
                marketplace=JPG_STORE,
                price=int(listing["price_lovelace"]) // 10**6,
                currency=self.currency,
                listed_at=listed_at,
                listed_by=None,
                tx_hash=listing["tx_hash"],
                marketplace_url=f"https://www.jpg.store/asset/{asset_id}",
            )

    def get_floor(self, collection_id: str, discriminator: str = None, *args, **kwargs) -> FloorDTO:
        self.check_collection_id(collection_id)

        floor = None
        count = 0

        for listing in self.get_listings(collection_id, discriminator=discriminator):
            count += 1

            if floor is None:
                floor = listing
            elif listing.usd < floor.usd:
                floor = listing

        return FloorDTO(
            listing=floor,
            listing_count=count,
        )

    def get_sales(self, collection_id: str, discriminator: str = None, *args, **kwargs) -> Iterable[SaleDTO]:
        self.check_collection_id(collection_id)

        for sale in jpgstore.get_sales(collection_id):
            tx_hash = sale["tx_hash"]

            asset_id = sale["asset_id"]
            policy_id, asset_name = utils.split_asset_id(asset_id)

            # required for multi-book policies (e.g. monsters, greek classics)
            if discriminator:
                if discriminator not in asset_name.lower():
                    continue

            if sale["action"] == "ACCEPT_OFFER":
                buyer = sale["seller_address"]
                seller = sale["signer_address"]
                sale_type = SaleType.OFFER
            elif sale["action"] == "ACCEPT_COLLECTION_OFFER":
                buyer = sale["signer_address"]
                seller = sale["seller_address"]
                sale_type = SaleType.COLLECTION_OFFER
            else:
                buyer = sale["signer_address"]
                seller = sale["seller_address"]

                if buyer == WINTER_NFT_ADDRESS:
                    sale_type = SaleType.CREDIT_CARD
                else:
                    sale_type = SaleType.PURCHASE

            asset_ids = []
            asset_names = []

            if sale["listing_from_tx_history"]["bundled_assets"]:
                for bundled_asset in sale["listing_from_tx_history"]["bundled_assets"]:
                    asset_ids.append(bundled_asset["asset_id"])
                    asset_names.append(bundled_asset["display_name"])
            else:
                asset_ids.append(sale["asset_id"])
                asset_names.append(sale["display_name"])

            if sale.get("confirmed_at"):
                confirmed_at = datetime.fromisoformat(sale["confirmed_at"].replace("Z", "+00:00"))
            else:
                confirmed_at = datetime.now(tz=pytz.utc)

            yield SaleDTO(
                identifier=tx_hash,
                collection_id=policy_id,
                asset_ids=asset_ids,
                asset_names=asset_names,
                tx_hash=tx_hash,
                marketplace=JPG_STORE,
                price=int(sale["amount_lovelace"]) // 10**6,
                currency=self.currency,
                confirmed_at=confirmed_at,
                type=sale_type,
                sold_by=seller,
                bought_by=buyer,
                marketplace_url=f"https://www.jpg.store/asset/{asset_id}",
                explorer_url=f"https://cardanoscan.io/transaction/{tx_hash}",
            )
