from unittest.mock import patch

import pytest

from api.domain.telemetry import (
    ProduceTelemetryResult,
    ProduceTelemetryStatus,
)


@pytest.fixture(autouse=True)
def mock_produce():
    with patch('api.routers.telemetry.produce_telemetry_records') as mock:
        yield mock


def test_ingest_telemetry_returns_202_for_accepted_result(
        mock_produce,
        client,
        producer,
        settings,
        valid_telemetry_record,
):
    """Test accepted service result returns 202 response."""
    mock_produce.return_value = ProduceTelemetryResult(
        status=ProduceTelemetryStatus.ACCEPTED,
        accepted=1,
        skipped=0,
        errors={},
    )

    response = client.post('/telemetry', json=valid_telemetry_record)

    assert response.status_code == 202
    body = response.json()
    assert body['status'] == ProduceTelemetryStatus.ACCEPTED
    assert body['accepted'] == 1
    assert body['skipped'] == 0
    assert body['errors'] == {}

    mock_produce.assert_called_once_with(
        payload=valid_telemetry_record,
        producer=producer,
        settings=settings,
    )


def test_ingest_telemetry_returns_422_for_rejected_result(
        mock_produce,
        client,
        producer,
        settings,
        valid_telemetry_record,
):
    """Test rejected service result returns 422 response."""
    mock_produce.return_value = ProduceTelemetryResult(
        status=ProduceTelemetryStatus.REJECTED,
        accepted=0,
        skipped=1,
        errors={0: 'invalid'},
    )

    response = client.post('/telemetry', json=[valid_telemetry_record, 'invalid'])

    assert response.status_code == 422
    body = response.json()
    assert body['status'] == ProduceTelemetryStatus.REJECTED
    assert body['accepted'] == 0
    assert body['skipped'] == 1
    assert '0' in body['errors']

    mock_produce.assert_called_once_with(
        payload=[valid_telemetry_record, 'invalid'],
        producer=producer,
        settings=settings,
    )


def test_ingest_telemetry_returns_503_for_unavailable_result(
        mock_produce,
        client,
        producer,
        settings,
        valid_telemetry_record,
):
    """Test unavailable service result returns 503 response."""
    mock_produce.return_value = ProduceTelemetryResult(
        status=ProduceTelemetryStatus.UNAVAILABLE,
        accepted=0,
        skipped=0,
        errors={0: 'failed'},
    )

    response = client.post('/telemetry', json=[valid_telemetry_record])

    assert response.status_code == 503
    body = response.json()
    assert body['status'] == ProduceTelemetryStatus.UNAVAILABLE
    assert body['accepted'] == 0
    assert body['skipped'] == 0
    assert '0' in body['errors']

    mock_produce.assert_called_once_with(
        payload=[valid_telemetry_record],
        producer=producer,
        settings=settings,
    )


def test_ingest_telemetry_invalid_top_level_payload_returns_422(
        mock_produce,
        client,
):
    """Test invalid top-level payload returns 422 and skips service."""
    response = client.post('/telemetry', json='invalid-payload')

    assert response.status_code == 422
    mock_produce.assert_not_called()
