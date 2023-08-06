from datetime import datetime
from typing import Any, List, Literal, Union

from pydantic import Field

from .base_model import BaseModel
from .enums import ComparisonOperator, DecisionBoundsType, NotificationSeverity
from .fragments import SegmentDetails


class GetValidatorSegmentIncidents(BaseModel):
    validator_segment_incidents: List[
        "GetValidatorSegmentIncidentsValidatorSegmentIncidents"
    ] = Field(alias="validatorSegmentIncidents")


class GetValidatorSegmentIncidentsValidatorSegmentIncidents(BaseModel):
    id: Any
    severity: NotificationSeverity
    segment: "GetValidatorSegmentIncidentsValidatorSegmentIncidentsSegment"
    metric: Union[
        "GetValidatorSegmentIncidentsValidatorSegmentIncidentsMetricValidatorMetric",
        "GetValidatorSegmentIncidentsValidatorSegmentIncidentsMetricValidatorMetricWithFixedThreshold",
        "GetValidatorSegmentIncidentsValidatorSegmentIncidentsMetricValidatorMetricWithDynamicThreshold",
        "GetValidatorSegmentIncidentsValidatorSegmentIncidentsMetricValidatorMetricWithMonotonicThreshold",
    ] = Field(discriminator="typename__")


class GetValidatorSegmentIncidentsValidatorSegmentIncidentsSegment(SegmentDetails):
    pass


class GetValidatorSegmentIncidentsValidatorSegmentIncidentsMetricValidatorMetric(
    BaseModel
):
    typename__: Literal["ValidatorMetric"] = Field(alias="__typename")
    start_time: datetime = Field(alias="startTime")
    end_time: datetime = Field(alias="endTime")
    is_incident: bool = Field(alias="isIncident")
    value: float


class GetValidatorSegmentIncidentsValidatorSegmentIncidentsMetricValidatorMetricWithFixedThreshold(
    BaseModel
):
    typename__: Literal["ValidatorMetricWithFixedThreshold"] = Field(alias="__typename")
    start_time: datetime = Field(alias="startTime")
    end_time: datetime = Field(alias="endTime")
    is_incident: bool = Field(alias="isIncident")
    value: float
    operator: ComparisonOperator
    bound: float


class GetValidatorSegmentIncidentsValidatorSegmentIncidentsMetricValidatorMetricWithDynamicThreshold(
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


class GetValidatorSegmentIncidentsValidatorSegmentIncidentsMetricValidatorMetricWithMonotonicThreshold(
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


GetValidatorSegmentIncidents.update_forward_refs()
GetValidatorSegmentIncidentsValidatorSegmentIncidents.update_forward_refs()
GetValidatorSegmentIncidentsValidatorSegmentIncidentsSegment.update_forward_refs()
GetValidatorSegmentIncidentsValidatorSegmentIncidentsMetricValidatorMetric.update_forward_refs()
GetValidatorSegmentIncidentsValidatorSegmentIncidentsMetricValidatorMetricWithFixedThreshold.update_forward_refs()
GetValidatorSegmentIncidentsValidatorSegmentIncidentsMetricValidatorMetricWithDynamicThreshold.update_forward_refs()
GetValidatorSegmentIncidentsValidatorSegmentIncidentsMetricValidatorMetricWithMonotonicThreshold.update_forward_refs()
