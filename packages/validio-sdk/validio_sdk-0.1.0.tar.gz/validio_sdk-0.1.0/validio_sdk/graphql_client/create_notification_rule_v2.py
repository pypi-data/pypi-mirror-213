from pydantic import Field

from .base_model import BaseModel
from .fragments import NotificationRuleV2Creation


class CreateNotificationRuleV2(BaseModel):
    notification_rule_v2_create: "CreateNotificationRuleV2NotificationRuleV2Create" = (
        Field(alias="notificationRuleV2Create")
    )


class CreateNotificationRuleV2NotificationRuleV2Create(NotificationRuleV2Creation):
    pass


CreateNotificationRuleV2.update_forward_refs()
CreateNotificationRuleV2NotificationRuleV2Create.update_forward_refs()
