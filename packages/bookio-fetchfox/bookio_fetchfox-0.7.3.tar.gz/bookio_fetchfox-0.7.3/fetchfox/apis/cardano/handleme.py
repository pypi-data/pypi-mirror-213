import logging
from functools import lru_cache
from typing import Tuple

from fetchfox import rest
from fetchfox.checks import check_str

BASE_URL = "https://api.handle.me"

logger = logging.getLogger(__name__)


def get(service: str, params: dict = None) -> Tuple[dict, int]:
    return rest.get(
        url=f"{BASE_URL}/{service}",
        params=params or {},
    )


@lru_cache
def resolve_handle(handle: str) -> str:
    check_str(handle)

    if handle.startswith("$"):
        handle = handle[1:]

    response, status_code = get(f"handles/{handle}")

    stake_address = response.get("holder_address")

    if not stake_address:
        return None

    logger.info("resolved $%s to %s", handle, stake_address)
    return stake_address


@lru_cache
def get_handle(stake_address: str) -> str:
    check_str(stake_address)

    response, status_code = get(f"holders/{stake_address}")

    handle = response.get("default_handle")

    if not handle:
        return None

    logger.info("resolved $%s to %s", stake_address, handle)
    return handle
