from __future__ import annotations
from typing import Tuple, Any
import attrs
from attrs import Attribute


def _validate_tiles(
    instance: Any, attribute: Attribute, value: Tuple[int, ...]
) -> None:
    if len(value) != 9:
        raise ValueError("Tiles must contain exactly 9 elements")
    if set(value) != set(range(9)):
        raise ValueError("Tiles must be a permutation of numbers 0 through 8")


@attrs.define(frozen=True, slots=True)
class PuzzleState:
    tiles: Tuple[int, ...] = attrs.field(
        validator=attrs.validators.and_(
            attrs.validators.instance_of(tuple),  # type check
            attrs.validators.min_len(9),  # length ≥ 9
            attrs.validators.max_len(9),
            _validate_tiles,
        )
    )
