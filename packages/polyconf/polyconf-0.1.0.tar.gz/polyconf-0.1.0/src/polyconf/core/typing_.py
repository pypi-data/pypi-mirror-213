from __future__ import annotations

from typing import Any, TypeAlias, TypeGuard, Union


# Only the most primitive types, mappable to JSON.
# Reminder: "primitive" means primitive at all nested levels.
PrimitiveScalar: TypeAlias = str | int | bool | None
PrimitiveIndex: TypeAlias = str | int

PrimitiveType: TypeAlias = Union[PrimitiveScalar, "PrimitiveCollection"]

PrimitiveSet: TypeAlias = set[PrimitiveType]
PrimitiveList: TypeAlias = list[PrimitiveType]
PrimitiveDict: TypeAlias = dict[PrimitiveIndex, PrimitiveType]

PrimitiveCollection: TypeAlias = PrimitiveSet | PrimitiveList | PrimitiveDict


# There is no way to use the TypeAliases themselves with complex instance checks.
# For example, this does NOT work:
#   assert isinstance(obj, PrimitiveScalarType)
# Solving with TypeGuard helper functions.


def is_primitive_scalar(obj: Any) -> TypeGuard[PrimitiveScalar]:
    return True if obj is None else isinstance(obj, (str, int, bool))


def is_primitive_index(obj: Any) -> TypeGuard[PrimitiveIndex]:
    return isinstance(obj, (str, int))


def is_primitive_type(obj: Any) -> TypeGuard[PrimitiveType]:
    # In effect, this only type checks 1 level deep and calls it good enough.
    return any(
        [
            is_primitive_scalar(obj),
            # isinstance(obj, (list, set, dict)),
            is_primitive_collection(obj),
        ]
    )


def is_primitive_set(obj: Any) -> TypeGuard[PrimitiveSet]:
    return isinstance(obj, set) and all(is_primitive_type(m) for m in obj)


def is_primitive_list(obj: Any) -> TypeGuard[PrimitiveList]:
    return isinstance(obj, list) and all(is_primitive_type(m) for m in obj)


def is_primitive_dict(obj: Any) -> TypeGuard[PrimitiveDict]:
    return isinstance(obj, dict) and all(is_primitive_index(k) and is_primitive_type(v) for k, v in obj.items())


def is_primitive_collection(obj: Any) -> TypeGuard[PrimitiveCollection]:
    return is_primitive_set(obj) or is_primitive_list(obj) or is_primitive_dict(obj)


# Seems like this shouldn't be necessary, but it gets me unstuck.
def is_set_of_str(obj: Any) -> TypeGuard[set[str]]:
    if not isinstance(obj, set):
        return False
    return True if len(obj) == 0 else all(isinstance(value, str) for value in obj)


def is_list_of_str(obj: Any) -> TypeGuard[list[str]]:
    if not isinstance(obj, list):
        return False
    return True if len(obj) == 0 else all(isinstance(value, str) for value in obj)


def is_primitive_list_of_dict(obj: Any) -> TypeGuard[list[PrimitiveDict]]:
    if not isinstance(obj, list):
        return False
    return True if len(obj) == 0 else all(isinstance(value, dict) for value in obj)


# -------------------------------------------------------------------------
# def is_primitive_collection(obj: Any) -> TypeGuard[PrimitiveCollection]:
#     collection_is_valid = isinstance(obj, (set, list, dict))
#     if not collection_is_valid:
#         return False
#     if isinstance(obj, dict):
#         valid_keys = all(isinstance(key, (str, int)) for key in obj.keys())
#         valid_values = all(is_primitive_scalar(value) for value in obj.values())
#         return valid_keys and valid_values
#     # set or list
#     return all(is_primitive_scalar(value) for value in obj)
