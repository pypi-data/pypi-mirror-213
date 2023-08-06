from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from polyconf.core import typing_ as t

from .context import Context
from .datum import Datum


if TYPE_CHECKING:
    from logging import Logger


class Plugin(ABC):
    """Plugin base class.

    Except for a few Plugin-specific attributes, Plugin is intended to be _stateless_.
    Do not confuse with data that belongs in a Context.
    """

    name: str
    is_flat: bool = False

    def __init__(self, logger: Logger) -> None:
        self.logger = logger

    @abstractmethod
    def hydrate(self, context: Context) -> Context:
        ...

    def add_result(self, name: str, value: t.PrimitiveType | Datum, context: Context, source: str = "") -> None:
        if isinstance(value, Datum):
            context.result.add_child(datum=value)
            return

        qualified_source = f"{self.name}://{source}"

        # expansions = self.expand_implicit_nesting(name=name, value=value)
        # for _name, _value in expansions:
        #     self.logger.debug(f"add_result: Expanded: {name} --> {_name=}, {_value=}")
        #     context.result.assimilate(name=_name, data=_value, source=qualified_source, parent=context.result)

        e_name, e_value = self.expand_implicit_nesting(name=name, value=value)
        merge = "__" in name
        # final_repr = f'{lb}"{top_name}": {lb}"{sub_name}": "{value}"{rb}{rb}'
        self.logger.debug(f"Assimilate:  {e_name}={e_value}")
        context.result.assimilate(
            name=e_name,
            data=e_value,
            source=qualified_source,
            parent=context.result,
            merge=merge,
        )
        context.result.traverse()

        # context.result.assimilate(name=name, data=value, source=qualified_source, parent=context.result)

    def expand_implicit_nesting(self, name: str, value: t.PrimitiveType) -> tuple[str, t.PrimitiveType]:
        if "__" not in name:
            return name, value

        top_name, _, sub_name = name.partition("__")

        lb = "{"
        rb = "}"
        old_repr = f'{lb}"{name}": "{value}"{rb}'
        new_repr = f'{lb}"{top_name}": {lb}"{sub_name}": "{value}"{rb}{rb}'
        self.logger.debug(f"Implicit name expansion:  {old_repr}  --> becomes -->  {new_repr}")

        while "__" in sub_name:
            self.logger.debug("More implicit nesting found: recursing...")
            sub_name, value = self.expand_implicit_nesting(sub_name, value)

        return top_name, {sub_name: value}

    # def expand_nested(self, datum: Datum) -> Datum:
    #     ...


# Dict entry 0 has incompatible type
# "str": "Union[
#   Union[str, int, bool, None],
#   Union[
#       Set[
#           Union[
#               Union[str, int, bool, None],
#           Union[
#               Set[Union[str, int, bool, None]], List[Union[str, int, bool, None]], Dict[Union[str, int], Union[str, int, bool, None]]]]], List[Union[Union[str, int, bool, None], Union[Set[Union[str, int, bool, None]], List[Union[str, int, bool, None]], Dict[Union[str, int], Union[str, int, bool, None]]]]], Dict[Union[str, int], Union[Union[str, int, bool, None], Union[Set[Union[str, int, bool, None]], List[Union[str, int, bool, None]], Dict[Union[str, int], Union[str, int, bool, None]]]]]]]"; expected "Union[str, int]": "Union[str, int, None, Set[Union[str, int, bool, None]], List[Union[str, int, bool, None]], Dict[Union[str, int], Union[str, int, bool, None]]]"  [dict-item]


# Dict entry 0 has incompatible type "str": "Union[Union[str, int, bool, None], Union[Set[Union[Union[str, int, bool, None], Union[Set[Union[str, int, bool, None]], List[Union[str, int, bool, None]], Dict[Union[str, int], Union[str, int, bool, None]]]]], List[Union[Union[str, int, bool, None], Union[Set[Union[str, int, bool, None]], List[Union[str, int, bool, None]], Dict[Union[str, int], Union[str, int, bool, None]]]]], Dict[Union[str, int], Union[Union[str, int, bool, None], Union[Set[Union[str, int, bool, None]], List[Union[str, int, bool, None]], Dict[Union[str, int], Union[str, int, bool, None]]]]]]]"; expected "Union[str, int]": "Union[str, int, None, Set[Union[str, int, bool, None]], List[Union[str, int, bool, None]], Dict[Union[str, int], Union[str, int, bool, None]]]"  [dict-item]
