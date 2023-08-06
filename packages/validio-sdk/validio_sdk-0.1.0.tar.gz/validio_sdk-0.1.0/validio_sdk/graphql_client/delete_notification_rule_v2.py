from pydantic import Field

from .base_model import BaseModel
from .fragments import NotificationRuleV2Deletion


class DeleteNotificationRuleV2(BaseModel):
    notification_rule_v2_delete: "DeleteNotificationRuleV2NotificationRuleV2Delete" = (
        Field(alias="notificationRuleV2Delete")
    )


class DeleteNotificationRuleV2NotificationRuleV2Delete(NotificationRuleV2Deletion):
    pass


DeleteNotificationRuleV2.update_forward_refs()
DeleteNotificationRuleV2NotificationRuleV2Delete.update_forward_refs()
