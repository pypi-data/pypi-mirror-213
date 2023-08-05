import logging
from functools import lru_cache
from typing import Tuple

from fetchfox import rest
from fetchfox.checks import check_str

BASE_URL = "https://api.nf.domains"

logger = logging.getLogger(__name__)


def get(service: str, params: dict = None) -> Tuple[dict, int]:
    return rest.get(
        url=f"{BASE_URL}/{service}",
        params=params or {},
    )


@lru_cache
def resolve_nf_domain(nf_domain: str):
    check_str(nf_domain, "nfddomains.nf_domain")

    response, status_code = get(
        "nfd",
        params={
            "prefix": nf_domain,
            "limit": 1,
        },
    )

    if not response:
        return None

    address = response[0]["owner"]
    logger.info("resolved %s to %s", nf_domain, address)

    return address


@lru_cache
def get_nf_domain(address: str):
    check_str(address, "nfddomains.address")
    address = address.upper()

    response, status_code = get(
        f"nfd/v2/address",
        params={
            "address": address,
        },
    )

    nf_domains = sorted(
        set(
            map(
                lambda nfd: nfd["name"],
                response[address],
            )
        ),
        key=len,
    )

    if not nf_domains:
        return None

    nf_domain = nf_domains[0]
    logger.info("resolved %s to %s", address, nf_domain)

    return nf_domain
