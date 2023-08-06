from typing import List

from pydantic import Field

from .base_model import BaseModel
from .enums import SourceState
from .fragments import ErrorDetails


class StopSource(BaseModel):
    source_stop: "StopSourceSourceStop" = Field(alias="sourceStop")


class StopSourceSourceStop(BaseModel):
    errors: List["StopSourceSourceStopErrors"]
    state: SourceState


class StopSourceSourceStopErrors(ErrorDetails):
    pass


StopSource.update_forward_refs()
StopSourceSourceStop.update_forward_refs()
StopSourceSourceStopErrors.update_forward_refs()
