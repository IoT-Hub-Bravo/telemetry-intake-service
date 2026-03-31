from dataclasses import FrozenInstanceError

import pytest

from api.domain.telemetry import (
    ProduceTelemetryResult,
    ProduceTelemetryStatus,
)


def test_result_defaults_to_empty_counters():
    """Test result uses zero counters and empty errors by default."""
    result = ProduceTelemetryResult(status=ProduceTelemetryStatus.ACCEPTED)

    assert result.status == ProduceTelemetryStatus.ACCEPTED
    assert result.accepted == 0
    assert result.skipped == 0
    assert result.errors == {}


def test_result_stores_provided_values():
    """Test result keeps explicitly provided status, counters, and errors."""
    errors = {1: 'invalid item', 'payload': 'invalid payload'}

    result = ProduceTelemetryResult(
        status=ProduceTelemetryStatus.REJECTED,
        accepted=2,
        skipped=3,
        errors=errors,
    )

    assert result.status == ProduceTelemetryStatus.REJECTED
    assert result.accepted == 2
    assert result.skipped == 3
    assert result.errors == errors


def test_result_is_immutable():
    """Test result cannot be modified after creation."""
    result = ProduceTelemetryResult(status=ProduceTelemetryStatus.ACCEPTED)

    with pytest.raises(FrozenInstanceError):
        result.accepted = 1
