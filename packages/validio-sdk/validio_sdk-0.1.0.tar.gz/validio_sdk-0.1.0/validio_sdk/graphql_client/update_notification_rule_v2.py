from pydantic import Field

from .base_model import BaseModel
from .fragments import NotificationRuleV2Update


class UpdateNotificationRuleV2(BaseModel):
    notification_rule_v2_update: "UpdateNotificationRuleV2NotificationRuleV2Update" = (
        Field(alias="notificationRuleV2Update")
    )


class UpdateNotificationRuleV2NotificationRuleV2Update(NotificationRuleV2Update):
    pass


UpdateNotificationRuleV2.update_forward_refs()
UpdateNotificationRuleV2NotificationRuleV2Update.update_forward_refs()
