"""Copyright (c) Modding Forge."""

MOD_UID_PART_BITS: int = 32
"""Number of bits assigned to each component of a Nexus Mods mod UID."""

MOD_UID_PART_MASK: int = (1 << MOD_UID_PART_BITS) - 1
"""Bit mask used to extract the game and mod identifiers."""

MAX_MOD_UID: int = (1 << (MOD_UID_PART_BITS * 2)) - 1
"""Largest supported unsigned Nexus Mods mod UID."""


def decode_mod_uid(uid: str) -> tuple[int, int]:
    """Decodes a decimal Nexus Mods mod UID into game and mod identifiers.

    Args:
        uid (str): Decimal 64-bit Nexus Mods mod UID.

    Returns:
        tuple[int, int]: Game identifier followed by mod identifier.

    Raises:
        ValueError: If the UID is not an unsigned decimal 64-bit integer.
    """

    try:
        value: int = int(uid)
    except ValueError as error:
        raise ValueError("The mod UID must be an unsigned decimal integer.") from error
    if value < 0 or value > MAX_MOD_UID:
        raise ValueError("The mod UID must fit in an unsigned 64-bit integer.")
    game_id: int = value >> MOD_UID_PART_BITS
    mod_id: int = value & MOD_UID_PART_MASK
    return game_id, mod_id
