from __future__ import annotations


class Endianness:
    BIG: Endianness = ...
    LITTLE: Endianness = ...

    def __repr__(self) -> str:
        ...


class TieBreaking:
    AWAY_FROM_ZERO: TieBreaking = ...
    TO_EVEN: TieBreaking = ...
    TO_ODD: TieBreaking = ...
    TOWARD_ZERO: TieBreaking = ...

    def __repr__(self) -> str:
        ...
