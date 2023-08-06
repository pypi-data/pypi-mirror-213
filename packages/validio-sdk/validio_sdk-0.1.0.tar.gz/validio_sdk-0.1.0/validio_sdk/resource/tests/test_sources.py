import pytest

from validio_sdk.resource._errors import ManifestConfigurationError
from validio_sdk.resource._resource import ResourceGraph
from validio_sdk.resource.credentials import GcpCredential
from validio_sdk.resource.sources import GcpBigQuerySource


@pytest.mark.parametrize(
    ("lookback_days", "schedule"),
    [
        (366, "* * * * *"),
        (2, "* * * * * *"),
    ],
)
def test_gcp_bigquery_source_invalid(lookback_days, schedule):
    c = GcpCredential(name="c1", credential="svc-acct", __internal__=ResourceGraph())
    with pytest.raises(ManifestConfigurationError):
        GcpBigQuerySource(
            name="s1",
            credential=c,
            project="proj",
            dataset="dataset",
            table="tab",
            cursor_field="curs",
            lookback_days=lookback_days,
            schedule=schedule,
        )
