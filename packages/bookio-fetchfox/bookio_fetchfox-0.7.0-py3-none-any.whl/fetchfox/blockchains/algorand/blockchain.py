import logging
from datetime import datetime
from typing import Iterable

import pytz

from fetchfox.apis.algorand import (
    algonodecloud,
    nfdomains,
    randswapcom,
    algoxnftcom,
    nftexplorerapp,
)
from fetchfox.blockchains.base import Blockchain
from fetchfox.constants.blockchains import ALGORAND
from fetchfox.constants.currencies import ALGO
from fetchfox.constants.marketplaces import (
    ALGOXNFT_COM,
    RANDGALLERY_COM,
    SHUFL_APP,
    UNKNOWN,
)
from fetchfox.dtos import AssetDTO, CampaignDTO, FloorDTO, HoldingDTO, ListingDTO, SaleDTO
from . import utils

logger = logging.getLogger(__name__)


class Algorand(Blockchain):
    def __init__(self, nftexplorerapp_api_key: str = None):
        super().__init__(
            name=ALGORAND,
            currency=ALGO,
            logo="https://s2.coinmarketcap.com/static/img/coins/64x64/4030.png",
        )

        self.nftexplorerapp_api_key: str = nftexplorerapp_api_key

    def check_collection_id(self, collection_id: str):
        if not utils.is_address(collection_id):
            raise ValueError(f"{collection_id} is not a valid algorand creator address")

    def check_asset_id(self, asset_id: str):
        if not utils.is_asset_id(asset_id):
            raise ValueError(f"{asset_id} is not a valid algorand asset id")

    def check_wallet(self, wallet: str):
        if not utils.is_wallet(wallet):
            raise ValueError(f"{wallet} is not a valid algorand address or nfdomain")

    def explorer_url(self, collection_id: str) -> str:
        return f"https://algoexplorer.io/address/{collection_id}"

    def marketplace_url(self, collection_id: str) -> str:
        return f"https://www.randgallery.com/algo-collection/?address={collection_id}"

    def get_assets(self, collection_id: str, fetch_metadata: bool = True, *args, **kwargs) -> Iterable[AssetDTO]:
        self.check_collection_id(collection_id)

        for asset_id in algonodecloud.get_assets(collection_id):
            if fetch_metadata:
                yield self.get_asset(
                    collection_id=collection_id,
                    asset_id=str(asset_id),
                )
            else:
                yield AssetDTO(
                    collection_id=collection_id,
                    asset_id=str(asset_id),
                    metadata={},
                )

    def get_asset(self, collection_id: str, asset_id: str, *args, **kwargs) -> AssetDTO:
        self.check_collection_id(collection_id)
        self.check_asset_id(asset_id)

        data = algonodecloud.get_asset_data(asset_id)
        metadata = algonodecloud.get_asset_metadata(asset_id)
        metadata["name"] = data["name"]

        return AssetDTO(
            collection_id=collection_id,
            asset_id=asset_id,
            metadata=metadata,
        )

    def get_campaigns(self) -> Iterable[CampaignDTO]:
        return

    def get_holdings(self, wallet: str, *args, **kwargs) -> Iterable[HoldingDTO]:
        self.check_wallet(wallet)

        if utils.is_nf_domain(wallet):
            wallet = nfdomains.resolve_nf_domain(wallet)

        holdings = algonodecloud.get_holdings(wallet)

        for holding in holdings:
            asset_id = holding["asset-id"]
            quantity = holding["amount"]

            if quantity < 1:
                continue

            yield HoldingDTO(
                collection_id=None,
                asset_id=asset_id,
                address=wallet,
                quantity=quantity,
            )

    def get_snapshot(self, collection_id: str, *args, **kwargs) -> Iterable[HoldingDTO]:
        self.check_collection_id(collection_id)

        for asset in self.get_assets(collection_id, fetch_metadata=False):
            holding = algonodecloud.get_owner(
                str(asset.asset_id),
            )

            yield HoldingDTO(
                collection_id=asset.collection_id,
                asset_id=holding["asset_id"],
                address=holding["address"],
                quantity=holding["amount"],
            )

    def get_listings(self, collection_id: str, *args, **kwargs) -> Iterable[ListingDTO]:
        self.check_collection_id(collection_id)

        listings = randswapcom.get_listings(collection_id)

        for listing in listings:
            asset_id = str(listing["assetId"])
            asset_ids = [asset_id]
            asset_names = [""]

            listed_at = datetime.fromtimestamp(
                listing["timestamp"] // 1000,
            ).replace(
                tzinfo=pytz.UTC,
            )

            yield ListingDTO(
                identifier=listing["timestamp"],
                collection_id=collection_id,
                asset_ids=asset_ids,
                asset_names=asset_names,
                listing_id=listing["timestamp"],
                marketplace=RANDGALLERY_COM,
                price=listing["price"],
                currency=ALGO,
                listed_at=listed_at,
                listed_by=listing["sellerAddress"],
                marketplace_url=f"https://www.randgallery.com/algo-collection/?address={asset_id}",
            )

        listings = algoxnftcom.get_listings(collection_id)

        for listing in listings:
            asset_id = str(listing["asset_id"])
            asset_ids = [asset_id]
            asset_names = [""]

            listed_at = datetime.now(tz=pytz.utc)

            yield ListingDTO(
                identifier=listing["buy_it_now_listing_id"],
                collection_id=collection_id,
                asset_ids=asset_ids,
                asset_names=asset_names,
                listing_id=listing["buy_it_now_listing_id"],
                marketplace=ALGOXNFT_COM,
                price=listing["price"] // 10**6,
                currency=self.currency,
                listed_at=listed_at,
                listed_by=listing["seller"],
                marketplace_url=f"https://algoxnft.com/asset/{asset_id}",
            )

    def get_floor(self, collection_id: str, *args, **kwargs) -> FloorDTO:
        self.check_collection_id(collection_id)

        floor = None
        count = 0

        for listing in self.get_listings(collection_id):
            count += 1

            if floor is None:
                floor = listing
            elif listing.usd < floor.usd:
                floor = listing

        return FloorDTO(
            listing=floor,
            listing_count=count,
        )

    def get_sales(self, collection_id: str, *args, **kwargs) -> Iterable[SaleDTO]:
        self.check_collection_id(collection_id)

        venues = {
            "algoxnft": ALGOXNFT_COM,
            "randgallery": RANDGALLERY_COM,
            "shufl": SHUFL_APP,
            None: UNKNOWN,
        }

        sales = nftexplorerapp.get_sales(
            collection_id,
            api_key=self.nftexplorerapp_api_key,
        )

        for sale in sales:
            tx_hash = sale["txnId"]

            asset_id = str(sale["asset"])
            asset_name = sale["assetName"]

            confirmed_at = datetime.fromtimestamp(
                sale["epochMs"] // 1000,
            ).replace(
                tzinfo=pytz.UTC,
            )

            marketplace = venues[sale.get("venue")]

            if marketplace == RANDGALLERY_COM:
                marketplace_url = f"https://www.randgallery.com/algo-collection/?address={asset_id}"
            elif marketplace == ALGOXNFT_COM:
                marketplace_url = f"https://algoxnft.com/asset/{asset_id}"
            elif marketplace == SHUFL_APP:
                marketplace_url = f"https://shufl.app/detail/{asset_id}"
            else:
                marketplace_url = None

            yield SaleDTO(
                identifier=tx_hash,
                collection_id=collection_id,
                asset_ids=[asset_id],
                asset_names=[asset_name],
                tx_hash=tx_hash,
                marketplace=marketplace,
                price=sale["ualgos"] // 10**6,
                currency=self.currency,
                confirmed_at=confirmed_at,
                sold_by=sale["sender"],
                bought_by=sale["receiver"],
                marketplace_url=marketplace_url,
                explorer_url=f"https://algoexplorer.io/tx/{tx_hash}",
            )
