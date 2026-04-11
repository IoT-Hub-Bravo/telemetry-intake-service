from typing import Any

from iot_hub_shared.kafka_kit import KafkaProducer, ProduceResult

from api.core.settings import Settings
from api.domain.telemetry import (
    ProduceTelemetryResult,
    ProduceTelemetryStatus,
)


def produce_telemetry_records(
        *,
        payload: dict[str, Any] | list[Any],
        producer: KafkaProducer,
        settings: Settings,
) -> ProduceTelemetryResult:
    if isinstance(payload, dict):
        records = [payload]
    elif isinstance(payload, list):
        records = payload
    else:
        return ProduceTelemetryResult(
            status=ProduceTelemetryStatus.REJECTED,
            errors={'json': 'Payload must be a JSON object or a JSON array.'},
        )

    if len(records) == 0:
        return ProduceTelemetryResult(
            status=ProduceTelemetryStatus.REJECTED,
            errors={'payload': 'Payload array is empty.'},
        )

    accepted = 0
    skipped = 0
    errors: dict[str | int, str] = {}

    for index, record in enumerate(records):
        if not isinstance(record, dict):
            errors[index] = 'Payload items must be JSON objects.'
            skipped += 1
            continue

        key = record.get(settings.http_producer_key_field)
        result = producer.produce(payload=record, key=key)

        if result == ProduceResult.ENQUEUED:
            accepted += 1
        else:
            errors[index] = str(result)

    status = ProduceTelemetryStatus.ACCEPTED

    # no valid records provided (all skipped / empty list)
    if accepted == 0 and skipped > 0:
        status = ProduceTelemetryStatus.REJECTED

    # no records accepted (kafka issues)
    elif accepted == 0 and errors:
        status = ProduceTelemetryStatus.UNAVAILABLE

    return ProduceTelemetryResult(
        status=status,
        accepted=accepted,
        skipped=skipped,
        errors=errors,
    )
