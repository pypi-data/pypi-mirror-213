from datetime import datetime
from typing import Any, List, Literal, Union

from pydantic import Field

from .base_model import BaseModel
from .enums import ComparisonOperator, DecisionBoundsType, NotificationSeverity
from .fragments import SegmentDetails


class GetSegmentIncidents(BaseModel):
    segment_incidents: List["GetSegmentIncidentsSegmentIncidents"] = Field(
        alias="segmentIncidents"
    )


class GetSegmentIncidentsSegmentIncidents(BaseModel):
    id: Any
    severity: NotificationSeverity
    segment: "GetSegmentIncidentsSegmentIncidentsSegment"
    metric: Union[
        "GetSegmentIncidentsSegmentIncidentsMetricValidatorMetric",
        "GetSegmentIncidentsSegmentIncidentsMetricValidatorMetricWithFixedThreshold",
        "GetSegmentIncidentsSegmentIncidentsMetricValidatorMetricWithDynamicThreshold",
        "GetSegmentIncidentsSegmentIncidentsMetricValidatorMetricWithMonotonicThreshold",
    ] = Field(discriminator="typename__")


class GetSegmentIncidentsSegmentIncidentsSegment(SegmentDetails):
    pass


class GetSegmentIncidentsSegmentIncidentsMetricValidatorMetric(BaseModel):
    typename__: Literal["ValidatorMetric"] = Field(alias="__typename")
    start_time: datetime = Field(alias="startTime")
    end_time: datetime = Field(alias="endTime")
    is_incident: bool = Field(alias="isIncident")
    value: float


class GetSegmentIncidentsSegmentIncidentsMetricValidatorMetricWithFixedThreshold(
    BaseModel
):
    typename__: Literal["ValidatorMetricWithFixedThreshold"] = Field(alias="__typename")
    start_time: datetime = Field(alias="startTime")
    end_time: datetime = Field(alias="endTime")
    is_incident: bool = Field(alias="isIncident")
    value: float
    operator: ComparisonOperator
    bound: float


class GetSegmentIncidentsSegmentIncidentsMetricValidatorMetricWithDynamicThreshold(
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


class GetSegmentIncidentsSegmentIncidentsMetricValidatorMetricWithMonotonicThreshold(
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


GetSegmentIncidents.update_forward_refs()
GetSegmentIncidentsSegmentIncidents.update_forward_refs()
GetSegmentIncidentsSegmentIncidentsSegment.update_forward_refs()
GetSegmentIncidentsSegmentIncidentsMetricValidatorMetric.update_forward_refs()
GetSegmentIncidentsSegmentIncidentsMetricValidatorMetricWithFixedThreshold.update_forward_refs()
GetSegmentIncidentsSegmentIncidentsMetricValidatorMetricWithDynamicThreshold.update_forward_refs()
GetSegmentIncidentsSegmentIncidentsMetricValidatorMetricWithMonotonicThreshold.update_forward_refs()
