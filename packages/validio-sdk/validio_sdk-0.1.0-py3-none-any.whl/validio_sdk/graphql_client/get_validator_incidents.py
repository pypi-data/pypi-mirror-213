from datetime import datetime
from typing import Any, List, Literal, Union

from pydantic import Field

from .base_model import BaseModel
from .enums import ComparisonOperator, DecisionBoundsType, NotificationSeverity
from .fragments import SegmentDetails


class GetValidatorIncidents(BaseModel):
    validator_incidents: List["GetValidatorIncidentsValidatorIncidents"] = Field(
        alias="validatorIncidents"
    )


class GetValidatorIncidentsValidatorIncidents(BaseModel):
    id: Any
    severity: NotificationSeverity
    segment: "GetValidatorIncidentsValidatorIncidentsSegment"
    metric: Union[
        "GetValidatorIncidentsValidatorIncidentsMetricValidatorMetric",
        "GetValidatorIncidentsValidatorIncidentsMetricValidatorMetricWithFixedThreshold",
        "GetValidatorIncidentsValidatorIncidentsMetricValidatorMetricWithDynamicThreshold",
        "GetValidatorIncidentsValidatorIncidentsMetricValidatorMetricWithMonotonicThreshold",
    ] = Field(discriminator="typename__")


class GetValidatorIncidentsValidatorIncidentsSegment(SegmentDetails):
    pass


class GetValidatorIncidentsValidatorIncidentsMetricValidatorMetric(BaseModel):
    typename__: Literal["ValidatorMetric"] = Field(alias="__typename")
    start_time: datetime = Field(alias="startTime")
    end_time: datetime = Field(alias="endTime")
    is_incident: bool = Field(alias="isIncident")
    value: float


class GetValidatorIncidentsValidatorIncidentsMetricValidatorMetricWithFixedThreshold(
    BaseModel
):
    typename__: Literal["ValidatorMetricWithFixedThreshold"] = Field(alias="__typename")
    start_time: datetime = Field(alias="startTime")
    end_time: datetime = Field(alias="endTime")
    is_incident: bool = Field(alias="isIncident")
    value: float
    operator: ComparisonOperator
    bound: float


class GetValidatorIncidentsValidatorIncidentsMetricValidatorMetricWithDynamicThreshold(
    BaseModel
):
    typename__: Literal["ValidatorMetricWithDynamicThreshold"] = Field(
        alias="__typename"
    )
    start_time: datetime = Field(alias="startTime")
    end_time: datetime = Field(alias="endTime")
    is_incident: bool = Field(alias="isIncident")
    value: float
    lower_bound: float = Field(alias="lowerBound")
    upper_bound: float = Field(alias="upperBound")
    decision_bounds_type: DecisionBoundsType = Field(alias="decisionBoundsType")
    is_burn_in: bool = Field(alias="isBurnIn")


class GetValidatorIncidentsValidatorIncidentsMetricValidatorMetricWithMonotonicThreshold(
    BaseModel
):
    typename__: Literal["ValidatorMetricWithMonotonicThreshold"] = Field(
        alias="__typename"
    )
    start_time: datetime = Field(alias="startTime")
    end_time: datetime = Field(alias="endTime")
    is_incident: bool = Field(alias="isIncident")
    value: float
    operator: ComparisonOperator


GetValidatorIncidents.update_forward_refs()
GetValidatorIncidentsValidatorIncidents.update_forward_refs()
GetValidatorIncidentsValidatorIncidentsSegment.update_forward_refs()
GetValidatorIncidentsValidatorIncidentsMetricValidatorMetric.update_forward_refs()
GetValidatorIncidentsValidatorIncidentsMetricValidatorMetricWithFixedThreshold.update_forward_refs()
GetValidatorIncidentsValidatorIncidentsMetricValidatorMetricWithDynamicThreshold.update_forward_refs()
GetValidatorIncidentsValidatorIncidentsMetricValidatorMetricWithMonotonicThreshold.update_forward_refs()
