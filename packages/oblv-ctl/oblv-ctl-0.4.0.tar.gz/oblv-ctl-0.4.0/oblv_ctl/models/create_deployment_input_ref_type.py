from enum import Enum


class CreateDeploymentInputRefType(str, Enum):
    BRANCH = "branch"
    TAG = "tag"

    def __str__(self) -> str:
        return str(self.value)
