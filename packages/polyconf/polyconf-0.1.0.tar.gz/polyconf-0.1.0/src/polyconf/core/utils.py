from functools import reduce
from typing import TypeVar


_InstanceType = TypeVar("_InstanceType")
_PipelineStepType = TypeVar("_PipelineStepType")
_ReturnType = TypeVar("_ReturnType")


def pipe(
    instance: _InstanceType,
    *functions: _PipelineStepType,
) -> _ReturnType:  # type: ignore[type-var]
    """
    Allows to compose a value and up to multiple functions that use this value.

    All starts with the value itself.
    Each next function uses the previous result as an input parameter.

    Currently, ``pipe`` has a hard limit of 21 steps.
    Because, it is not possible to type it otherwise.
    We need a hard limit.
    See: https://github.com/dry-python/returns/issues/461

    Here's how it should be used:

    .. code:: python

       >>> # => executes: str(float(int('1')))
       >>> assert pipe('1', int, float, str) == '1.0'

    See also:
        - https://stackoverflow.com/a/41585450/4842742
        - https://github.com/gcanti/fp-ts/blob/master/src/pipeable.ts

    Note:
        Vendored from:
            https://github.com/dry-python/returns/blob/master/returns/_internal/pipeline/flow.py

        Edits:
            - Reduced irrelevant info in the docstring content to avoid confusion.
            - Renamed "flow" to "pipe".
    """
    return reduce(  # type: ignore
        lambda composed, function: function(composed),  # type: ignore
        functions,
        instance,
    )
