from typing import Any, Callable, Dict

from validio_sdk.scalars import (
    EnumFilter,
    NullFilter,
    StringFilter,
    ThresholdFilter,
    serialize_json_filter_expression,
)

SCALARS_PARSE_FUNCTIONS: Dict[Any, Callable[[Any], Any]] = {}
SCALARS_SERIALIZE_FUNCTIONS: Dict[Any, Callable[[Any], Any]] = {
    EnumFilter: serialize_json_filter_expression,
    NullFilter: serialize_json_filter_expression,
    StringFilter: serialize_json_filter_expression,
    ThresholdFilter: serialize_json_filter_expression,
}
