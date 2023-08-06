from enum import Enum


class StaticDeploymentInputInfraReqs(str, Enum):
    C5_2XLARGE = "c5.2xlarge"
    C5_XLARGE = "c5.xlarge"
    M5_2XLARGE = "m5.2xlarge"
    M5_4XLARGE = "m5.4xlarge"
    M5_XLARGE = "m5.xlarge"
    R5_XLARGE = "r5.xlarge"

    def __str__(self) -> str:
        return str(self.value)
