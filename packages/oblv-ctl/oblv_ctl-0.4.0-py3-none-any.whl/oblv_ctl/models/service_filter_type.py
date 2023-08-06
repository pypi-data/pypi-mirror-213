from enum import Enum


class ServiceFilterType(str, Enum):
    ALL = "all"
    MARKETPLACE = "marketplace"
    PRIVATE = "private"

    def __str__(self) -> str:
        return str(self.value)
