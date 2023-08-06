from enum import Enum


class CreateDeploymentInputAccountType(str, Enum):
    GITHUB = "github"

    def __str__(self) -> str:
        return str(self.value)
