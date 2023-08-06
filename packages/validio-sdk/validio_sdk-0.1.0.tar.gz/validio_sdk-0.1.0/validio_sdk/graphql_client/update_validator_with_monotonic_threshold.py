from datetime import datetime
from typing import Annotated, List, Literal, Optional, Union

from pydantic import Field

from validio_sdk.scalars import (
    DestinationId,
    JsonFilterExpression,
    JsonPointer,
    SegmentationId,
    SourceId,
    ValidatorId,
    WindowId,
)

from .base_model import BaseModel
from .enums import (
    CategoricalDistributionMetric,
    ComparisonOperator,
    DecisionBoundsType,
    NumericAnomalyMetric,
    NumericDistributionMetric,
    NumericMetric,
    RelativeTimeMetric,
    RelativeVolumeMetric,
    VolumeMetric,
)
from .fragments import ErrorDetails


class UpdateValidatorWithMonotonicThreshold(BaseModel):
    validator_with_monotonic_threshold_update: "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdate" = Field(
        alias="validatorWithMonotonicThresholdUpdate"
    )


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdate(
    BaseModel
):
    errors: List[
        "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateErrors"
    ]
    validator: Optional[
        Annotated[
            Union[
                "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorValidator",
                "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericValidator",
                "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorCategoricalDistributionValidator",
                "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericDistributionValidator",
                "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorVolumeValidator",
                "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericAnomalyValidator",
                "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorRelativeTimeValidator",
                "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorFreshnessValidator",
                "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorRelativeVolumeValidator",
            ],
            Field(discriminator="typename__"),
        ]
    ]


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateErrors(
    ErrorDetails
):
    pass


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorValidator(
    BaseModel
):
    typename__: Literal["Validator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorValidatorSourceConfig" = Field(
        alias="sourceConfig"
    )
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorValidatorSourceConfig(
    BaseModel
):
    source: "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorValidatorSourceConfigSource"
    window: "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorValidatorSourceConfigWindow"
    segmentation: "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorValidatorSourceConfigSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorValidatorSourceConfigWindow(
    BaseModel
):
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorValidatorSourceConfigSegmentation(
    BaseModel
):
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericValidator(
    BaseModel
):
    typename__: Literal["NumericValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericValidatorSourceConfig" = Field(
        alias="sourceConfig"
    )
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericValidatorConfig"


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericValidatorSourceConfig(
    BaseModel
):
    source: "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericValidatorSourceConfigSource"
    window: "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericValidatorSourceConfigWindow"
    segmentation: "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericValidatorSourceConfigSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericValidatorSourceConfigWindow(
    BaseModel
):
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericValidatorSourceConfigSegmentation(
    BaseModel
):
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericValidatorConfig(
    BaseModel
):
    source_field: JsonPointer = Field(alias="sourceField")
    metric: NumericMetric
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericValidatorConfigThresholdDynamicThreshold",
        "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericValidatorConfigThresholdFixedThreshold",
        "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericValidatorConfigThresholdMonotonicThreshold",
    ] = Field(discriminator="typename__")


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericValidatorConfigThresholdMonotonicThreshold(
    BaseModel
):
    typename__: Literal["MonotonicThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorCategoricalDistributionValidator(
    BaseModel
):
    typename__: Literal["CategoricalDistributionValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfig" = Field(
        alias="sourceConfig"
    )
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorCategoricalDistributionValidatorConfig"
    reference_source_config: "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfig" = Field(
        alias="referenceSourceConfig"
    )


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfig(
    BaseModel
):
    source: "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSource"
    window: "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigWindow"
    segmentation: "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigWindow(
    BaseModel
):
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSegmentation(
    BaseModel
):
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorCategoricalDistributionValidatorConfig(
    BaseModel
):
    source_field: JsonPointer = Field(alias="sourceField")
    reference_source_field: JsonPointer = Field(alias="referenceSourceField")
    categorical_distribution_metric: CategoricalDistributionMetric = Field(
        alias="categoricalDistributionMetric"
    )
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorCategoricalDistributionValidatorConfigThresholdDynamicThreshold",
        "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorCategoricalDistributionValidatorConfigThresholdFixedThreshold",
        "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorCategoricalDistributionValidatorConfigThresholdMonotonicThreshold",
    ] = Field(discriminator="typename__")


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorCategoricalDistributionValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorCategoricalDistributionValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorCategoricalDistributionValidatorConfigThresholdMonotonicThreshold(
    BaseModel
):
    typename__: Literal["MonotonicThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfig(
    BaseModel
):
    source: "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSource"
    window: "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigWindow"
    history: int
    offset: int
    filter: Optional[JsonFilterExpression]


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigWindow(
    BaseModel
):
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericDistributionValidator(
    BaseModel
):
    typename__: Literal["NumericDistributionValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericDistributionValidatorSourceConfig" = Field(
        alias="sourceConfig"
    )
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericDistributionValidatorConfig"
    reference_source_config: "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfig" = Field(
        alias="referenceSourceConfig"
    )


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericDistributionValidatorSourceConfig(
    BaseModel
):
    source: "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSource"
    window: "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigWindow"
    segmentation: "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigWindow(
    BaseModel
):
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSegmentation(
    BaseModel
):
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericDistributionValidatorConfig(
    BaseModel
):
    source_field: JsonPointer = Field(alias="sourceField")
    reference_source_field: JsonPointer = Field(alias="referenceSourceField")
    distribution_metric: NumericDistributionMetric = Field(alias="distributionMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericDistributionValidatorConfigThresholdDynamicThreshold",
        "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericDistributionValidatorConfigThresholdFixedThreshold",
        "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericDistributionValidatorConfigThresholdMonotonicThreshold",
    ] = Field(discriminator="typename__")


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericDistributionValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericDistributionValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericDistributionValidatorConfigThresholdMonotonicThreshold(
    BaseModel
):
    typename__: Literal["MonotonicThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfig(
    BaseModel
):
    source: "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSource"
    window: "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigWindow"
    history: int
    offset: int
    filter: Optional[JsonFilterExpression]


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigWindow(
    BaseModel
):
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorVolumeValidator(
    BaseModel
):
    typename__: Literal["VolumeValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorVolumeValidatorSourceConfig" = Field(
        alias="sourceConfig"
    )
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorVolumeValidatorConfig"
    destination: Optional[
        "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorVolumeValidatorDestination"
    ]


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorVolumeValidatorSourceConfig(
    BaseModel
):
    source: "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorVolumeValidatorSourceConfigSource"
    window: "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorVolumeValidatorSourceConfigWindow"
    segmentation: "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorVolumeValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorVolumeValidatorSourceConfigSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorVolumeValidatorSourceConfigWindow(
    BaseModel
):
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorVolumeValidatorSourceConfigSegmentation(
    BaseModel
):
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorVolumeValidatorConfig(
    BaseModel
):
    optional_source_field: Optional[JsonPointer] = Field(alias="optionalSourceField")
    source_fields: List[JsonPointer] = Field(alias="sourceFields")
    volume_metric: VolumeMetric = Field(alias="volumeMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorVolumeValidatorConfigThresholdDynamicThreshold",
        "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorVolumeValidatorConfigThresholdFixedThreshold",
        "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorVolumeValidatorConfigThresholdMonotonicThreshold",
    ] = Field(discriminator="typename__")


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorVolumeValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorVolumeValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorVolumeValidatorConfigThresholdMonotonicThreshold(
    BaseModel
):
    typename__: Literal["MonotonicThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorVolumeValidatorDestination(
    BaseModel
):
    name: str
    id: DestinationId
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericAnomalyValidator(
    BaseModel
):
    typename__: Literal["NumericAnomalyValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfig" = Field(
        alias="sourceConfig"
    )
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericAnomalyValidatorConfig"
    reference_source_config: "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfig" = Field(
        alias="referenceSourceConfig"
    )
    destination: Optional[
        "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericAnomalyValidatorDestination"
    ]


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfig(
    BaseModel
):
    source: "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSource"
    window: "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigWindow"
    segmentation: "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigWindow(
    BaseModel
):
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSegmentation(
    BaseModel
):
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericAnomalyValidatorConfig(
    BaseModel
):
    source_field: JsonPointer = Field(alias="sourceField")
    numeric_anomaly_metric: NumericAnomalyMetric = Field(alias="numericAnomalyMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericAnomalyValidatorConfigThresholdDynamicThreshold",
        "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericAnomalyValidatorConfigThresholdFixedThreshold",
        "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericAnomalyValidatorConfigThresholdMonotonicThreshold",
    ] = Field(discriminator="typename__")
    reference_source_field: JsonPointer = Field(alias="referenceSourceField")
    sensitivity: float
    minimum_reference_datapoints: Optional[float] = Field(
        alias="minimumReferenceDatapoints"
    )
    minimum_absolute_difference: float = Field(alias="minimumAbsoluteDifference")
    minimum_relative_difference_percent: float = Field(
        alias="minimumRelativeDifferencePercent"
    )


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericAnomalyValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericAnomalyValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericAnomalyValidatorConfigThresholdMonotonicThreshold(
    BaseModel
):
    typename__: Literal["MonotonicThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfig(
    BaseModel
):
    source: "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSource"
    window: "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigWindow"
    history: int
    offset: int
    filter: Optional[JsonFilterExpression]


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigWindow(
    BaseModel
):
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericAnomalyValidatorDestination(
    BaseModel
):
    name: str
    id: DestinationId
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorRelativeTimeValidator(
    BaseModel
):
    typename__: Literal["RelativeTimeValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorRelativeTimeValidatorSourceConfig" = Field(
        alias="sourceConfig"
    )
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorRelativeTimeValidatorConfig"


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorRelativeTimeValidatorSourceConfig(
    BaseModel
):
    source: "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSource"
    window: "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigWindow"
    segmentation: "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigWindow(
    BaseModel
):
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSegmentation(
    BaseModel
):
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorRelativeTimeValidatorConfig(
    BaseModel
):
    source_field_minuend: JsonPointer = Field(alias="sourceFieldMinuend")
    source_field_subtrahend: JsonPointer = Field(alias="sourceFieldSubtrahend")
    relative_time_metric: RelativeTimeMetric = Field(alias="relativeTimeMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorRelativeTimeValidatorConfigThresholdDynamicThreshold",
        "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorRelativeTimeValidatorConfigThresholdFixedThreshold",
        "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorRelativeTimeValidatorConfigThresholdMonotonicThreshold",
    ] = Field(discriminator="typename__")


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorRelativeTimeValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorRelativeTimeValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorRelativeTimeValidatorConfigThresholdMonotonicThreshold(
    BaseModel
):
    typename__: Literal["MonotonicThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorFreshnessValidator(
    BaseModel
):
    typename__: Literal["FreshnessValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorFreshnessValidatorSourceConfig" = Field(
        alias="sourceConfig"
    )
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorFreshnessValidatorConfig"


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorFreshnessValidatorSourceConfig(
    BaseModel
):
    source: "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorFreshnessValidatorSourceConfigSource"
    window: "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorFreshnessValidatorSourceConfigWindow"
    segmentation: "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorFreshnessValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorFreshnessValidatorSourceConfigSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorFreshnessValidatorSourceConfigWindow(
    BaseModel
):
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorFreshnessValidatorSourceConfigSegmentation(
    BaseModel
):
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorFreshnessValidatorConfig(
    BaseModel
):
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorFreshnessValidatorConfigThresholdDynamicThreshold",
        "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorFreshnessValidatorConfigThresholdFixedThreshold",
        "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorFreshnessValidatorConfigThresholdMonotonicThreshold",
    ] = Field(discriminator="typename__")


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorFreshnessValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorFreshnessValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorFreshnessValidatorConfigThresholdMonotonicThreshold(
    BaseModel
):
    typename__: Literal["MonotonicThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorRelativeVolumeValidator(
    BaseModel
):
    typename__: Literal["RelativeVolumeValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfig" = Field(
        alias="sourceConfig"
    )
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorRelativeVolumeValidatorConfig"
    reference_source_config: "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfig" = Field(
        alias="referenceSourceConfig"
    )


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfig(
    BaseModel
):
    source: "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSource"
    window: "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigWindow"
    segmentation: "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigWindow(
    BaseModel
):
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSegmentation(
    BaseModel
):
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorRelativeVolumeValidatorConfig(
    BaseModel
):
    optional_source_field: Optional[JsonPointer] = Field(alias="optionalSourceField")
    optional_reference_source_field: Optional[JsonPointer] = Field(
        alias="optionalReferenceSourceField"
    )
    relative_volume_metric: RelativeVolumeMetric = Field(alias="relativeVolumeMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorRelativeVolumeValidatorConfigThresholdDynamicThreshold",
        "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorRelativeVolumeValidatorConfigThresholdFixedThreshold",
        "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorRelativeVolumeValidatorConfigThresholdMonotonicThreshold",
    ] = Field(discriminator="typename__")


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorRelativeVolumeValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorRelativeVolumeValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorRelativeVolumeValidatorConfigThresholdMonotonicThreshold(
    BaseModel
):
    typename__: Literal["MonotonicThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfig(
    BaseModel
):
    source: "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSource"
    window: "UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigWindow"
    history: int
    offset: int
    filter: Optional[JsonFilterExpression]


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigWindow(
    BaseModel
):
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


UpdateValidatorWithMonotonicThreshold.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdate.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateErrors.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorValidator.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorValidatorSourceConfig.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorValidatorSourceConfigSource.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorValidatorSourceConfigWindow.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorValidatorSourceConfigSegmentation.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericValidator.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericValidatorSourceConfig.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericValidatorSourceConfigSource.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericValidatorSourceConfigWindow.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericValidatorSourceConfigSegmentation.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericValidatorConfig.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericValidatorConfigThresholdDynamicThreshold.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericValidatorConfigThresholdFixedThreshold.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericValidatorConfigThresholdMonotonicThreshold.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorCategoricalDistributionValidator.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfig.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSource.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigWindow.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSegmentation.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorCategoricalDistributionValidatorConfig.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorCategoricalDistributionValidatorConfigThresholdDynamicThreshold.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorCategoricalDistributionValidatorConfigThresholdFixedThreshold.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorCategoricalDistributionValidatorConfigThresholdMonotonicThreshold.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfig.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSource.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigWindow.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericDistributionValidator.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericDistributionValidatorSourceConfig.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSource.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigWindow.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSegmentation.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericDistributionValidatorConfig.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericDistributionValidatorConfigThresholdDynamicThreshold.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericDistributionValidatorConfigThresholdFixedThreshold.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericDistributionValidatorConfigThresholdMonotonicThreshold.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfig.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSource.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigWindow.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorVolumeValidator.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorVolumeValidatorSourceConfig.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorVolumeValidatorSourceConfigSource.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorVolumeValidatorSourceConfigWindow.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorVolumeValidatorSourceConfigSegmentation.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorVolumeValidatorConfig.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorVolumeValidatorConfigThresholdDynamicThreshold.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorVolumeValidatorConfigThresholdFixedThreshold.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorVolumeValidatorConfigThresholdMonotonicThreshold.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorVolumeValidatorDestination.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericAnomalyValidator.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfig.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSource.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigWindow.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSegmentation.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericAnomalyValidatorConfig.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericAnomalyValidatorConfigThresholdDynamicThreshold.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericAnomalyValidatorConfigThresholdFixedThreshold.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericAnomalyValidatorConfigThresholdMonotonicThreshold.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfig.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSource.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigWindow.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorNumericAnomalyValidatorDestination.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorRelativeTimeValidator.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorRelativeTimeValidatorSourceConfig.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSource.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigWindow.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSegmentation.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorRelativeTimeValidatorConfig.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorRelativeTimeValidatorConfigThresholdDynamicThreshold.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorRelativeTimeValidatorConfigThresholdFixedThreshold.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorRelativeTimeValidatorConfigThresholdMonotonicThreshold.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorFreshnessValidator.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorFreshnessValidatorSourceConfig.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorFreshnessValidatorSourceConfigSource.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorFreshnessValidatorSourceConfigWindow.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorFreshnessValidatorSourceConfigSegmentation.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorFreshnessValidatorConfig.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorFreshnessValidatorConfigThresholdDynamicThreshold.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorFreshnessValidatorConfigThresholdFixedThreshold.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorFreshnessValidatorConfigThresholdMonotonicThreshold.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorRelativeVolumeValidator.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfig.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSource.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigWindow.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSegmentation.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorRelativeVolumeValidatorConfig.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorRelativeVolumeValidatorConfigThresholdDynamicThreshold.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorRelativeVolumeValidatorConfigThresholdFixedThreshold.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorRelativeVolumeValidatorConfigThresholdMonotonicThreshold.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfig.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSource.update_forward_refs()
UpdateValidatorWithMonotonicThresholdValidatorWithMonotonicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigWindow.update_forward_refs()
