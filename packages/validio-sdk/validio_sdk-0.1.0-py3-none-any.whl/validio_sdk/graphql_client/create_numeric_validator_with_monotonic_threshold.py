from pydantic import Field

from .base_model import BaseModel
from .fragments import ValidatorCreation


class CreateNumericValidatorWithMonotonicThreshold(BaseModel):
    numeric_validator_with_monotonic_threshold_create: "CreateNumericValidatorWithMonotonicThresholdNumericValidatorWithMonotonicThresholdCreate" = Field(
        alias="numericValidatorWithMonotonicThresholdCreate"
    )


class CreateNumericValidatorWithMonotonicThresholdNumericValidatorWithMonotonicThresholdCreate(
    ValidatorCreation
):
    pass


CreateNumericValidatorWithMonotonicThreshold.update_forward_refs()
CreateNumericValidatorWithMonotonicThresholdNumericValidatorWithMonotonicThresholdCreate.update_forward_refs()
