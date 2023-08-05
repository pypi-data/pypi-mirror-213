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
            POLYGON,
            MATIC,
            moralisio_api_key=moralisio_api_key,
            openseaio_api_key=openseaio_api_key,
        )
