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
            name=ETHEREUM,
            currency=ETH,
            logo="https://s2.coinmarketcap.com/static/img/coins/64x64/1027.png",
            moralisio_api_key=moralisio_api_key,
            openseaio_api_key=openseaio_api_key,
        )

    def explorer_url(self, collection_id: str) -> str:
        return f"https://etherscan.io/address/{collection_id}"
