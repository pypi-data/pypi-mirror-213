from fetchfox.blockchains.evm import Evm
from fetchfox.constants.blockchains import ETHEREUM
from fetchfox.constants.currencies import ETH


class Ethereum(Evm):
    def __init__(
        self,
        moralisio_api_key: str = None,
        openseaio_api_key: str = None,
    ):
        super().__init__(
            ETHEREUM,
            ETH,
            moralisio_api_key=moralisio_api_key,
            openseaio_api_key=openseaio_api_key,
        )
