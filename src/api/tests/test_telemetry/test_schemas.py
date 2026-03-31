from api.domain.telemetry import ProduceTelemetryStatus
from api.schemas.telemetry import (
    BaseTelemetryResponse,
    TelemetryAcceptedResponse,
    TelemetryRejectedResponse,
    TelemetryUnavailableResponse,
)


def test_base_response_stores_provided_values():
    """Test base response keeps provided status, counters, and errors."""
    errors = {1: 'invalid item', 'payload': 'invalid payload'}

    response = BaseTelemetryResponse(
        status=ProduceTelemetryStatus.ACCEPTED,
        accepted=2,
        skipped=1,
        errors=errors,
    )

    assert response.status == ProduceTelemetryStatus.ACCEPTED
    assert response.accepted == 2
    assert response.skipped == 1
    assert response.errors == errors


def test_accepted_response_uses_accepted_status_by_default():
    """Test accepted response uses accepted status by default."""
    response = TelemetryAcceptedResponse(accepted=3, skipped=1)

    assert response.status == ProduceTelemetryStatus.ACCEPTED
    assert response.accepted == 3
    assert response.skipped == 1
    assert response.errors == {}


def test_rejected_response_uses_rejected_status_and_zero_accepted():
    """Test rejected response uses rejected status and zero accepted by default."""
    response = TelemetryRejectedResponse(skipped=2)

    assert response.status == ProduceTelemetryStatus.REJECTED
    assert response.accepted == 0
    assert response.skipped == 2
    assert response.errors == {}


def test_unavailable_response_uses_unavailable_status_and_zero_accepted():
    """Test unavailable response uses unavailable status and zero accepted by default."""
    response = TelemetryUnavailableResponse(skipped=0)

    assert response.status == ProduceTelemetryStatus.UNAVAILABLE
    assert response.accepted == 0
    assert response.skipped == 0
    assert response.errors == {}


def test_response_errors_default_is_not_shared():
    """Test each response instance has its own errors."""
    errors = {'payload': 'invalid'}
    first = TelemetryAcceptedResponse(accepted=1, skipped=0, errors=errors)
    second = TelemetryAcceptedResponse(accepted=1, skipped=0)

    assert first.errors == errors
    assert second.errors == {}
