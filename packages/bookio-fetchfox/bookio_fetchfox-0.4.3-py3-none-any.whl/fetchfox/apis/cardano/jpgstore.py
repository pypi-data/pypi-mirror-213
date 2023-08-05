import logging
from typing import Iterable, Tuple

from fetchfox import rest
from fetchfox.checks import check_str

BASE_URL = "https://server.jpgstoreapis.com"

logger = logging.getLogger(__name__)


def get(service: str, params: dict = None) -> Tuple[dict, int]:
    return rest.get(
        url=f"{BASE_URL}/{service}",
        params=params or {},
        sleep=0.5,
    )


def get_listings(policy_id: str) -> Iterable[dict]:
    check_str(policy_id, "jpgstore.policy_id")
    policy_id = policy_id.strip().lower()

    cursor = ""

    while True:
        params = {}

        if cursor:
            params["cursor"] = cursor

        response, status_code = get(
            f"policy/{policy_id}/listings",
            params=params,
        )

        cursor = response.get("nextPageCursor")

        if not cursor:  # pragma: no cover
            break

        yield from response["listings"]


def get_sales(policy_id: str) -> Iterable[dict]:
    check_str(policy_id, "jpgstore.policy_id")
    policy_id = policy_id.strip().lower()

    txs = set()

    page = 0

    while True:
        page += 1

        if page > 200:
            break

        response, status_code = get(
            f"collection/{policy_id}/transactions",
            params={
                "page": page,
                "count": 50,
            },
        )

        if not response:  # pragma: no cover
            break

        for sale in response["transactions"]:
            tx_hash = sale["tx_hash"]

            if tx_hash in txs:
                continue

            txs.add(tx_hash)

            yield sale
