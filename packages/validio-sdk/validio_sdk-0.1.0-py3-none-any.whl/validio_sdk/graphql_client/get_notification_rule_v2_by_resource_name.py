from typing import Optional

from pydantic import Field

from .base_model import BaseModel
from .fragments import NotificationRuleV2Details


class GetNotificationRuleV2ByResourceName(BaseModel):
    notification_rule_v2_by_resource_name: Optional[
        "GetNotificationRuleV2ByResourceNameNotificationRuleV2ByResourceName"
    ] = Field(alias="notificationRuleV2ByResourceName")


class GetNotificationRuleV2ByResourceNameNotificationRuleV2ByResourceName(
    NotificationRuleV2Details
):
    pass


GetNotificationRuleV2ByResourceName.update_forward_refs()
GetNotificationRuleV2ByResourceNameNotificationRuleV2ByResourceName.update_forward_refs()
