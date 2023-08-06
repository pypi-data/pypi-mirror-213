from fetchfox.blockchains.evm import Evm
from fetchfox.constants.blockchains import POLYGON
from fetchfox.constants.currencies import MATIC


class Polygon(Evm):
    def __init__(
        self,
        moralisio_api_key: str = None,
        openseaio_api_key: str = None,
    ):
        super().__init__(
            name=POLYGON,
            currency=MATIC,
            logo="https://s2.coinmarketcap.com/static/img/coins/64x64/3890.png",
            moralisio_api_key=moralisio_api_key,
            openseaio_api_key=openseaio_api_key,
        )

    def explorer_url(self, collection_id: str) -> str:
        return f"https://polygonscan.com/address/{collection_id}"
