from enum import StrEnum, auto


class NotFoundComponentsPolicy(StrEnum):
    IGNORE = auto()
    ABORT = auto()
