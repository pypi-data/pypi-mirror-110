from typing import Optional, List, TypeVar, Generic

import discord.ui

from .item import Item
from .select_option import SelectOption
from .custom import CustomSelect


C = TypeVar("C", bound=discord.ui.Select)


class Select(Item, Generic[C]):
    def __init__(
            self,
            placeholder: Optional[str] = None,
            min_values: int = 1,
            max_values: int = 1,
            options: Optional[list] = None,
            cls: C = CustomSelect
    ) -> None:
        self._placeholder: Optional[str] = placeholder
        self._min_values: int = min_values
        self._max_values: int = max_values
        self._options: list = [] if options is None else options
        self._row: Optional[int] = None
        self.cls: C = cls

    def placeholder(self, placeholder: str) -> 'Select':
        self._placeholder = placeholder
        return self

    def min_values(self, min_values: int) -> 'Select':
        self._min_values = min_values
        return self

    def max_values(self, max_values: int) -> 'Select':
        self._max_values = max_values
        return self

    def options(self, options: List[SelectOption]) -> 'Select':
        self._options = options
        return self

    def row(self, row: int) -> 'Select':
        self._row = row
        return self

    def to_discord(self) -> C:
        return self.cls(
            placeholder=self._placeholder,
            min_values=self._min_values,
            max_values=self._max_values,
            options=[o.to_discord_select_option() for o in self._options],
            row=self._row
        )
