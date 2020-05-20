from itertools import chain
from typing import Any, Text


class UnchangeableMixIn:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __setattr__(self, key: Text, value: Any) -> None:
        if hasattr(self, key):
            raise AttributeError(
                f"{self.__class__.__name__} "
                f"attributes can be added but not modified."
                f"Attribute {key!r} already exists with value"
                f" {getattr(self, key)!r}"
            )
        self.__dict__[key] = value

    def __eq__(self, rhs: "UnchangeableMixIn") -> bool:
        if type(self) is not type(rhs):
            return NotImplemented
        return self.__dict__ == rhs.__dict__

    def __ne__(self, rhs: "UnchangeableMixIn") -> bool:
        return not self == rhs

    def __hash__(self) -> int:
        return hash(tuple(chain(self.__dict__.items(), [type(self)])))

    def __repr__(self) -> Text:
        args = ', '.join(
            f"{key}={value!r}" for key, value in self.__dict__.items()
        )
        return f'{self.__class__.__qualname__}({args})'
