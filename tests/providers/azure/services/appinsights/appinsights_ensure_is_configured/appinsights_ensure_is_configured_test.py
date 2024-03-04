from unittest import mock

from prowler.providers.azure.services.appinsights.appinsights_service import Component
from tests.providers.azure.azure_fixtures import AZURE_SUBSCRIPTION


class Test_appinsights_ensure_is_configured:
    def test_appinsights_no_subscriptions(self):
        appinsights_client = mock.MagicMock
        appinsights_client.components = {}

        with mock.patch(
            "prowler.providers.azure.services.appinsights.appinsights_ensure_is_configured.appinsights_ensure_is_configured.appinsights_client",
            new=appinsights_client,
        ):
            from prowler.providers.azure.services.appinsights.appinsights_ensure_is_configured.appinsights_ensure_is_configured import (
                appinsights_ensure_is_configured,
            )

            check = appinsights_ensure_is_configured()
            result = check.execute()
            assert len(result) == 0

    def test_no_appinsights(self):
        appinsights_client = mock.MagicMock
        appinsights_client.components = {AZURE_SUBSCRIPTION: {}}

        with mock.patch(
            "prowler.providers.azure.services.appinsights.appinsights_ensure_is_configured.appinsights_ensure_is_configured.appinsights_client",
            new=appinsights_client,
        ):
            from prowler.providers.azure.services.appinsights.appinsights_ensure_is_configured.appinsights_ensure_is_configured import (
                appinsights_ensure_is_configured,
            )

            check = appinsights_ensure_is_configured()
            result = check.execute()
            assert len(result) == 1
            assert result[0].subscription == AZURE_SUBSCRIPTION
            assert result[0].status == "FAIL"
            assert result[0].resource_id == "AppInsights"
            assert result[0].resource_name == "AppInsights"
            assert (
                result[0].status_extended
                == f"There are no AppInsight configured in susbscription {AZURE_SUBSCRIPTION}."
            )

    def test_appinsights_configured(self):
        appinsights_client = mock.MagicMock
        appinsights_client.components = {
            AZURE_SUBSCRIPTION: {
                "app_id-1": Component(
                    resource_id="/subscriptions/resource_id",
                    resource_name="AppInsightsTest",
                )
            }
        }

        with mock.patch(
            "prowler.providers.azure.services.appinsights.appinsights_ensure_is_configured.appinsights_ensure_is_configured.appinsights_client",
            new=appinsights_client,
        ):
            from prowler.providers.azure.services.appinsights.appinsights_ensure_is_configured.appinsights_ensure_is_configured import (
                appinsights_ensure_is_configured,
            )

            check = appinsights_ensure_is_configured()
            result = check.execute()
            assert len(result) == 1
            assert result[0].subscription == AZURE_SUBSCRIPTION
            assert result[0].status == "PASS"
            assert result[0].resource_id == "AppInsights"
            assert result[0].resource_name == "AppInsights"
            assert (
                result[0].status_extended
                == f"There is at least one AppInsight configured in susbscription {AZURE_SUBSCRIPTION}."
            )
