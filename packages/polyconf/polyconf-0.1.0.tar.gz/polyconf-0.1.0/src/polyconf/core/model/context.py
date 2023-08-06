from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .datum import Datum
from .status import Status, status_new


def root_datum() -> Datum:
    return Datum(name="root")


@dataclass
class Context:
    app_name: str
    app_prefix: str = ""
    trim_prefix: bool = True
    given: dict[str, Any] = field(default_factory=dict)
    status: Status = field(default_factory=status_new)
    result: Datum = field(default_factory=root_datum)

    def __post_init__(self) -> None:
        self.app_prefix = self.app_prefix or self.app_name.upper()

        if self.given:
            # self.result = {k: Datum(k, v, sources={"given"}) for k, v in self.given.items()}
            self.result = Datum.from_dict(data=self.given, source="given")
