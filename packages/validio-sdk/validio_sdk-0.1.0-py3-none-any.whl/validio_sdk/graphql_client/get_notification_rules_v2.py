from typing import List

from pydantic import Field

from .base_model import BaseModel
from .fragments import NotificationRuleV2Details


class GetNotificationRulesV2(BaseModel):
    notification_rules_v2: List["GetNotificationRulesV2NotificationRulesV2"] = Field(
        alias="notificationRulesV2"
    )


class GetNotificationRulesV2NotificationRulesV2(NotificationRuleV2Details):
    pass


GetNotificationRulesV2.update_forward_refs()
GetNotificationRulesV2NotificationRulesV2.update_forward_refs()
