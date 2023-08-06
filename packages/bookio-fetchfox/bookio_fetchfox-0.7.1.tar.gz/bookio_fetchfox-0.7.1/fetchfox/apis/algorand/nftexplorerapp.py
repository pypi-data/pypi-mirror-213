from functools import lru_cache
from typing import Iterable, Tuple

from fetchfox import rest
from fetchfox.checks import check_str

BASE_URL = "https://api.nftexplorer.app"


def get(service: str, api_key: str, params: dict = None, version: int = 1) -> Tuple[dict, int]:
    check_str(api_key, "nftexplorerapp.api_key")

    return rest.get(
        url=f"{BASE_URL}/v{version}/{service}",
        headers={
            "Authorization": api_key,
        },
        params=params or {},
        sleep=1,
    )


@lru_cache
def get_collection_id(creator_address: str, api_key: str) -> str:
    check_str(creator_address, "randswap.creator_address")
    creator_address = creator_address.upper()

    response, status_code = get(
        "collections/search",
        params={
            "q": creator_address,
        },
        api_key=api_key,
    )

    verified = response["results"].get("verified", [])

    if verified:
        return verified[0]["collectionId"]

    recognized = response["results"].get("recognized", [])

    if recognized:
        return recognized[0]["collectionId"]

    return None


def get_sales(creator_address: str, api_key: str) -> Iterable[dict]:
    check_str(creator_address, "randswap.creator_address")
    creator_address = creator_address.upper()

    collection_id = get_collection_id(creator_address, api_key)

    next_token = None

    while True:
        response, status_code = get(
            "/collections/salesHistory",
            params={
                "collectionId": collection_id,
                "nextToken": next_token,
            },
            api_key=api_key,
        )

        yield from response["sales"]

        next_token = response.get("nextToken")

        if not next_token:
            break
