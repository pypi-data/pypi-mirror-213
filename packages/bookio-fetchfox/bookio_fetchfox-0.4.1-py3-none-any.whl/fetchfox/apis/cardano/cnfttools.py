from typing import Iterable, Tuple

from fetchfox import rest

BASE_URL = "https://api.cnft.tools/api"


def get(service: str, params: dict = None) -> Tuple[dict, int]:
    return rest.get(
        url=f"{BASE_URL}/{service}",
        params=params or {},
    )


def get_ranks(policy_id: str) -> Iterable[dict]:
    response, status_code = get(f"rankings/{policy_id}")

    if response.get("error"):
        return

    yield from response.items()
