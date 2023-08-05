from abc import abstractmethod
from typing import Iterable, Optional

from fetchfox.apis import coingeckocom
from fetchfox.dtos import (
    AssetDTO,
    CampaignDTO,
    FloorDTO,
    HoldingDTO,
    ListingDTO,
    RankDTO,
    SaleDTO,
)


class Blockchain:
    def __init__(self, name: str, currency: str, logo: str):
        self.name: str = name
        self.currency: str = currency
        self.logo: str = logo

    def usd(self) -> float:
        return coingeckocom.usd(self.currency)

    @abstractmethod
    def check_collection_id(self, collection_id: str):
        raise NotImplementedError()

    @abstractmethod
    def check_asset_id(self, asset_id: str):
        raise NotImplementedError()

    @abstractmethod
    def check_wallet(self, wallet: str):
        raise NotImplementedError()

    @abstractmethod
    def get_assets(self, collection_id: str, fetch_metadata: bool = True, *args, **kwargs) -> Iterable[AssetDTO]:
        raise NotImplementedError()

    @abstractmethod
    def get_asset(self, collection_id: str, asset_id: str, *args, **kwargs) -> AssetDTO:
        raise NotImplementedError()

    def get_campaigns(self) -> Iterable[CampaignDTO]:
        raise NotImplementedError()

    @abstractmethod
    def get_holdings(self, wallet: str, *args, **kwargs) -> Iterable[HoldingDTO]:
        raise NotImplementedError()

    @abstractmethod
    def get_listings(self, collection_id: str, *args, **kwargs) -> Iterable[ListingDTO]:
        raise NotImplementedError()

    @abstractmethod
    def get_floor(self, collection_id: str, *args, **kwargs) -> FloorDTO:
        raise NotImplementedError()

    def get_rank(self, collection_id: str, asset_id: str, *args, **kwargs) -> RankDTO:
        raise NotImplementedError()

    def get_ranks(self, collection_id: str, *args, **kwargs) -> Iterable[RankDTO]:
        raise NotImplementedError()

    @abstractmethod
    def get_snapshot(self, collection_id: str, *args, **kwargs) -> Iterable[HoldingDTO]:
        raise NotImplementedError()

    @abstractmethod
    def get_sales(self, collection_id: str, *args, **kwargs) -> Iterable[SaleDTO]:
        raise NotImplementedError()
