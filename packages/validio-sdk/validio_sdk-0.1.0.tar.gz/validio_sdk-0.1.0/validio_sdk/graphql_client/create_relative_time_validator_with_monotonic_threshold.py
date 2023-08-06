from pydantic import Field

from .base_model import BaseModel
from .fragments import ValidatorCreation


class CreateRelativeTimeValidatorWithMonotonicThreshold(BaseModel):
    relative_time_validator_with_monotonic_threshold_create: "CreateRelativeTimeValidatorWithMonotonicThresholdRelativeTimeValidatorWithMonotonicThresholdCreate" = Field(
        alias="relativeTimeValidatorWithMonotonicThresholdCreate"
    )


class CreateRelativeTimeValidatorWithMonotonicThresholdRelativeTimeValidatorWithMonotonicThresholdCreate(
    ValidatorCreation
):
    pass


CreateRelativeTimeValidatorWithMonotonicThreshold.update_forward_refs()
CreateRelativeTimeValidatorWithMonotonicThresholdRelativeTimeValidatorWithMonotonicThresholdCreate.update_forward_refs()
