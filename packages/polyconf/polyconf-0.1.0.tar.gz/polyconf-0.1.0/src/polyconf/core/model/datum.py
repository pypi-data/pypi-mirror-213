"""Datum module."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Self, Type, TypeVar

from polyconf.core import typing_ as t
from polyconf.core.deepmerge import deep


T = TypeVar("T")


@dataclass
class Datum:
    """Atomic declaration of a data value.

    Attributes:
        name: The canonical name of the data value.  Required.
        value: For storing a scalar value.
        children: For storing a collection value.
        sources: A set recording everywhere the value was seen.

    Notes:
        The members of the "sources" attribute is a URI-like string, where the protocol is the plugin and the path is
        a description of the data source.

        Example:
            "file_yaml://.../foo.yaml"

        How strict this will be is TBD.  For now, it's loosely defined ad hoc.
    """

    name: t.PrimitiveIndex
    value: t.PrimitiveScalar = None
    children: set[Datum] = field(default_factory=set)
    sources: set[str] = field(default_factory=set)

    @property
    def children_names(self) -> set[t.PrimitiveIndex]:
        return {c.name for c in self.children}

    @property
    def as_native_value(self) -> t.PrimitiveType:
        # NOTE: currently not actively in use, but it seems useful and works well.
        if self.value is not None:
            return self.value
        elif self.children:
            if self.looks_like() == list:
                return [child.as_native_value for child in self.children]
            return {c.name: c.as_native_value for c in self.children}
        else:
            return None

    def add_child(self, datum: Datum, merge: bool = False) -> None:
        if existing_child := self.get(name=datum.name):
            # When exists, always drop first because "merge" intends to "replace".
            self.remove_child(datum)

            if merge:
                merged_child = existing_child | datum
                self.children.add(merged_child)
            else:
                self.children.add(datum)

        # New child
        else:
            self.children.add(datum)

    def remove_child(self, datum: Datum) -> None:
        if found_child := self.get(datum.name):
            self.children.remove(found_child)

        # Note: This is more well behaved than:
        # self.children.discard(datum)
        #   (or self.children.remove(datum))
        # because the native lookup is based on hash, while the desired basis is on name.

    def put(
        self,
        name: t.PrimitiveIndex,
        value: t.PrimitiveScalar = None,
        source: str | None = None,
        merge: bool = False,
    ) -> None:
        if name not in self.children_names:
            sources = set() if source is None else {source}
            self.add_child(Datum(name=name, value=value, sources=sources), merge=merge)
            return

        # TODO: Confirm these changes persist.
        if child_node := self.get(name=name):
            child_node.value = value
            if source:
                child_node.sources.add(source)

    def traverse(self) -> None:
        nodes_to_visit = [self]
        while nodes_to_visit:
            current_node = nodes_to_visit.pop()
            bad_state = all(
                [
                    current_node.value is not None,
                    current_node.children is not None,
                    len(current_node.children) > 0,
                ],
            )
            if bad_state:
                print("Encountered a bad state.  Dropping value in favor of children.")
                current_node.value = None

            nodes_to_visit += current_node.children

    def get(self, name: t.PrimitiveIndex, default: T | None = None) -> Datum | T | None:
        """Get child datum by name.

        Queries self.children for a matching "name" attribute.
        If not found, it returns a default, which may be specified by the caller.

        Args:
            name: The child datum name to retrieve.
            default: The default value to return if the child is not found.
                Defaults to None.
        """
        return next((child for child in self.children if child.name == name), default)

    def eq_helper(self) -> str:
        fields = [
            self.name,
            self.value,
            sorted(self.children),
            sorted(self.sources),
        ]
        return "|".join(repr(x) for x in fields)

    def looks_like(self) -> Type[str | int | bool | list[Any] | dict[Any, Any]]:
        if self.value is not None:
            return self.value.__class__

        first_index = list(self.children)[0].name
        if isinstance(first_index, int):
            return list
        elif isinstance(first_index, str):
            return dict
        else:
            raise TypeError(first_index)

    @classmethod
    def assimilate(
        cls,
        name: t.PrimitiveIndex,
        data: t.PrimitiveType,
        source: str,
        parent: Self,
        merge: bool = False,
    ) -> None:
        # Plain scalar value -- no recursion.
        if t.is_primitive_scalar(data) and data is not None:
            parent.put(name=name, value=data, source=source, merge=merge)

        # Container value -- perform recursion.
        elif t.is_primitive_dict(data):
            dict_node = cls(name=name, sources={source})
            for d_name, d_value in data.items():
                dict_node.assimilate(name=d_name, data=d_value, source=source, parent=dict_node)  # TODO typing
            parent.add_child(dict_node, merge=merge)
        elif t.is_primitive_list(data):
            # Wrap elements in a list-like node, where keys are integer indices.
            list_node = cls(name=name, sources={source})
            for i, member in enumerate(data):
                list_node.assimilate(name=i, data=member, source=source, parent=list_node)  # TODO typing
            parent.add_child(list_node, merge=merge)

        else:
            raise TypeError(data)

    @classmethod
    def from_dict(cls, data: dict[str, Any], source: str = "cls-factory") -> Self:
        root = cls(name="root", sources={source})
        for key, value in data.items():
            root.assimilate(name=key, data=value, source=source, parent=root)
        return root

    # def _is_valid_datum_serial(self, data: t.PrimitiveDict) -> bool:

    @classmethod
    def _deserialize(cls, data: t.PrimitiveDict, default_name: str = "root") -> Self:
        found_name = data.get("name", default_name)
        if not t.is_primitive_index(found_name):
            raise TypeError(f"Expected name to be str or int, got {found_name}.")

        found_value = data.get("value")
        if not t.is_primitive_scalar(found_value):
            raise TypeError(f"Expected value to be {t.PrimitiveScalar}, got {found_value}.")

        found_sources = data.get("sources", [])
        if not t.is_list_of_str(found_sources):
            raise TypeError(f"Expected sources to be a list[str], got {found_sources}.")

        new_datum = cls(
            name=found_name,
            value=found_value,
            sources=set(found_sources),
        )

        if data.get("value") is not None:
            return new_datum

        # if found_children := data.get("children") is not None:
        #     if len(found_children) > 0:
        #         for child in found_children:
        #             new_datum.add_child(cls._deserialize(child), merge=True)

        found_children = data.get("children", [])
        if not t.is_primitive_list_of_dict(found_children):
            raise TypeError(f"Expected children to be a list[dict], got {found_children}.")

        if found_children is not None:
            for child in found_children:
                new_datum.add_child(cls._deserialize(child), merge=True)

        return new_datum

    @classmethod
    def deserialize(cls, data: t.PrimitiveDict) -> Self:
        # # for key, value in data.items():
        # #     value
        # validations = [
        #     isinstance(data, dict),
        #     data.get("api") == "v1",
        #     data.get("name") == "root",
        # ]
        # if not all(validations):
        #     # raise TypeError(data)
        #     ...

        return cls._deserialize(data)

        # root = cls(name="root", value=data.get("value"), sources=data.get("sources"))
        #
        # if children := data.get("children"):
        #     root.children = cls._deserialize(children)

        # root = cls(name="root", sources={source})
        # for key, value in data.items():
        #     root.assimilate(name=key, data=value, source=source, parent=root)
        # return root

    def serialize(self) -> t.PrimitiveDict:
        data: t.PrimitiveDict = {
            "name": self.name,
        }
        if self.value is not None:
            data["value"] = self.value
        if self.children:
            data["children"] = [child.serialize() for child in sorted(self.children)]
        if self.sources:
            data["sources"] = list(self.sources)
        return data

    def __or__(self, other: Datum) -> Datum:
        if not isinstance(other, Datum):
            return NotImplemented

        self_dict = self.serialize()
        other_dict = other.serialize()
        # other_dict: dict = other.serialize() if isinstance(other, Datum) else other

        deep.merge(self_dict, other_dict)  # type:ignore

        return self.deserialize(self_dict)

    def __ror__(self, other: Datum) -> Datum:
        if not isinstance(other, Datum):
            return NotImplemented

        self_dict = self.serialize()
        other_dict = other.serialize()
        # other_dict: dict = other.serialize() if isinstance(other, Datum) else other

        deep.merge(other_dict, self_dict)  # type:ignore

        return self.deserialize(other_dict)

    # def __ior__(self, other: Datum) -> None:
    #     # I'm not sure if this is actually possible.
    #     # Keeping as a bookmark / note-to-self.
    #     raise NotImplemented

    def __getitem__(self, item: t.PrimitiveIndex) -> Datum | None:
        return self.get(item, default=None)

    def __contains__(self, item: Datum | str) -> bool:
        if isinstance(item, Datum):
            return item in self.children
        else:
            return item in self.children_names

    def __hash__(self) -> int:
        # return hash(f"{self.name}|{self.value}|{self.children_names}|{self.sources}")
        # return hash(self.name)
        return hash(self.eq_helper())

    def __eq__(self, other: Any) -> bool:
        # return hash(self) == hash(other)
        if not isinstance(other, Datum):
            return NotImplemented
        return self.eq_helper() == other.eq_helper()

    # Implementing the rest of these enables iterables of Datum to be sortable.
    def __lt__(self, other: Self) -> bool:
        return self.eq_helper() < other.eq_helper()

    def __le__(self, other: Self) -> bool:
        return self.eq_helper() <= other.eq_helper()

    def __gt__(self, other: Self) -> bool:
        return self.eq_helper() > other.eq_helper()

    def __ge__(self, other: Self) -> bool:
        return self.eq_helper() >= other.eq_helper()
