from unittest.mock import Mock, patch

from core.plugin.entities.plugin_daemon import CredentialType
from models.trigger import TriggerSubscription
from tasks.trigger_subscription_refresh_tasks import _refresh_subscription_if_expired


def _subscription(*, expires_at: int) -> TriggerSubscription:
    subscription = TriggerSubscription(
        tenant_id="tenant-1",
        user_id="user-1",
        name="gmail",
        endpoint_id="endpoint-1",
        provider_id="langgenius/gmail_trigger/gmail_trigger",
        parameters={},
        properties={},
        credentials={},
        credential_type=CredentialType.OAUTH2,
        expires_at=expires_at,
    )
    subscription.id = "subscription-1"
    return subscription


def test_refresh_subscription_if_expired_skips_never_expire_minus_one() -> None:
    with (
        patch(
            "tasks.trigger_subscription_refresh_tasks.dify_config",
            Mock(TRIGGER_PROVIDER_SUBSCRIPTION_THRESHOLD_SECONDS=3600),
        ),
        patch("tasks.trigger_subscription_refresh_tasks.TriggerProviderService.refresh_subscription") as refresh,
    ):
        _refresh_subscription_if_expired(
            tenant_id="tenant-1",
            subscription=_subscription(expires_at=-1),
            now=1_787_560_000,
        )

    refresh.assert_not_called()


def test_refresh_subscription_if_expired_uses_stored_expires_at() -> None:
    now = 1_787_560_000
    threshold = 3600
    due = _subscription(expires_at=now + threshold)
    not_due = _subscription(expires_at=now + threshold + 1)

    with (
        patch(
            "tasks.trigger_subscription_refresh_tasks.dify_config",
            Mock(TRIGGER_PROVIDER_SUBSCRIPTION_THRESHOLD_SECONDS=threshold),
        ),
        patch(
            "tasks.trigger_subscription_refresh_tasks.TriggerProviderService.refresh_subscription",
            return_value={"result": "success", "expires_at": now + 7 * 24 * 60 * 60},
        ) as refresh,
    ):
        _refresh_subscription_if_expired(tenant_id="tenant-1", subscription=not_due, now=now)
        refresh.assert_not_called()

        _refresh_subscription_if_expired(tenant_id="tenant-1", subscription=due, now=now)
        refresh.assert_called_once_with(tenant_id="tenant-1", subscription_id=due.id, now=now)
