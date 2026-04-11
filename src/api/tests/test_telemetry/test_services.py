from unittest.mock import call

import pytest
from iot_hub_shared.kafka_kit import ProduceResult

from api.domain.telemetry import ProduceTelemetryStatus
from api.services.telemetry_ingest import produce_telemetry_records


def test_ingest_invalid_payload_type_returns_rejected(producer, settings):
    """Test invalid top-level payload returns rejected result."""
    result = produce_telemetry_records(
        payload='invalid-payload',
        producer=producer,
        settings=settings,
    )

    assert result.status == ProduceTelemetryStatus.REJECTED
    assert result.accepted == 0
    assert result.skipped == 0
    assert 'json' in result.errors
    producer.produce.assert_not_called()


def test_ingest_empty_batch_returns_rejected(producer, settings):
    """Test empty batch returns rejected result."""
    result = produce_telemetry_records(
        payload=[],
        producer=producer,
        settings=settings,
    )

    assert result.status == ProduceTelemetryStatus.REJECTED
    assert result.accepted == 0
    assert result.skipped == 0
    assert 'payload' in result.errors
    producer.produce.assert_not_called()


def test_ingest_single_record_enqueues(producer, settings, valid_telemetry_record):
    """Test single record is sent to producer and accepted."""
    producer.produce.return_value = ProduceResult.ENQUEUED

    result = produce_telemetry_records(
        payload=valid_telemetry_record,
        producer=producer,
        settings=settings,
    )

    assert result.status == ProduceTelemetryStatus.ACCEPTED
    assert result.accepted == 1
    assert result.skipped == 0
    assert result.errors == {}
    producer.produce.assert_called_once_with(payload=valid_telemetry_record, key='SN-001')


def test_ingest_batch_skips_invalid_items_and_accepts_valid(
        producer,
        settings,
        valid_telemetry_record,
):
    """Test batch skips invalid items and processes valid records."""
    valid_record2 = dict(valid_telemetry_record)
    valid_record2['device_serial_id'] = 'SN-002'

    producer.produce.side_effect = [ProduceResult.ENQUEUED, ProduceResult.ENQUEUED]
    payload = [valid_telemetry_record, 'invalid', 123, valid_record2]

    result = produce_telemetry_records(
        payload=payload,
        producer=producer,
        settings=settings,
    )

    assert result.status == ProduceTelemetryStatus.ACCEPTED
    assert result.accepted == 2
    assert result.skipped == 2
    assert set(result.errors) == {1, 2}
    assert producer.produce.call_args_list == [
        call(payload=valid_telemetry_record, key='SN-001'),
        call(payload=valid_record2, key='SN-002'),
    ]


def test_ingest_batch_with_only_invalid_items_returns_rejected(producer, settings):
    """Test batch with only invalid items returns rejected result."""
    payload = ['invalid', 123, []]

    result = produce_telemetry_records(
        payload=payload,
        producer=producer,
        settings=settings,
    )

    assert result.status == ProduceTelemetryStatus.REJECTED
    assert result.accepted == 0
    assert result.skipped == 3
    assert set(result.errors) == {0, 1, 2}
    producer.produce.assert_not_called()


def test_ingest_batch_all_producer_failures_returns_unavailable(
        producer,
        settings,
        valid_telemetry_record,
):
    """Test batch with no accepted records returns unavailable."""
    producer.produce.side_effect = [ProduceResult.BUFFER_FULL, ProduceResult.BUFFER_FULL]

    result = produce_telemetry_records(
        payload=[valid_telemetry_record, valid_telemetry_record],
        producer=producer,
        settings=settings,
    )

    assert result.status == ProduceTelemetryStatus.UNAVAILABLE
    assert result.accepted == 0
    assert result.skipped == 0
    assert set(result.errors) == {0, 1}
    assert producer.produce.call_count == 2


def test_ingest_batch_partial_producer_failures_stays_accepted(
        producer,
        settings,
        valid_telemetry_record,
):
    """Test batch stays accepted when at least one record is enqueued."""
    producer.produce.side_effect = [ProduceResult.ENQUEUED, ProduceResult.BUFFER_FULL]

    result = produce_telemetry_records(
        payload=[valid_telemetry_record, valid_telemetry_record],
        producer=producer,
        settings=settings,
    )

    assert result.status == ProduceTelemetryStatus.ACCEPTED
    assert result.accepted == 1
    assert result.skipped == 0
    assert set(result.errors) == {1}
    assert producer.produce.call_count == 2
