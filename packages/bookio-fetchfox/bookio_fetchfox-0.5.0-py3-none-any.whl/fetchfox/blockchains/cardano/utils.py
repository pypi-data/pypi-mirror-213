from typing import Tuple

from fetchfox.blockchains.utils import check

ADA_HANDLE_REGEX = r"^\$[a-zA-Z0-9\-_.]{1,15}$"
SHORT_ADDRESS_REGEX = r"^addr1[0-9a-zA-Z]{53}$"
LONG_ADDRESS_REGEX = r"^addr1[0-9a-zA-Z]{98}$"
ASSET_ID_REGEX = r"^[a-fA-F0-9]{56}[a-fA-F0-9]+$"
POLICY_ID_REGEX = r"^[a-fA-F0-9]{56}$"
STAKE_KEY_REGEX = r"^stake1[0-9a-zA-Z]{53}$"


def is_ada_handle(string: str) -> bool:
    return check(ADA_HANDLE_REGEX, string)


def is_address(string) -> bool:
    if check(SHORT_ADDRESS_REGEX, string):
        return True

    return check(LONG_ADDRESS_REGEX, string)


def is_asset_id(string: str) -> bool:
    return check(ASSET_ID_REGEX, string)


def is_policy_id(string: str) -> bool:
    return check(POLICY_ID_REGEX, string)


def is_stake_key(string: str) -> bool:
    return check(STAKE_KEY_REGEX, string)


def split_asset_id(asset_id: str) -> Tuple[str, str]:
    return asset_id[:56], bytes.fromhex(asset_id[56:]).decode()


def is_wallet(wallet: str) -> bool:
    return is_stake_key(wallet) or is_address(wallet) or is_ada_handle(wallet)
