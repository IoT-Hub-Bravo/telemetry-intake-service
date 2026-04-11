from typing import Any, Annotated

from fastapi import APIRouter, Body, Depends
from fastapi.responses import JSONResponse
from iot_hub_shared.kafka_kit import KafkaProducer

from api.core.settings import Settings, get_settings
from api.dependencies import get_kafka_producer
from api.domain.telemetry import ProduceTelemetryStatus
from api.schemas.telemetry import (
    TelemetryAcceptedResponse,
    TelemetryRejectedResponse,
    TelemetryUnavailableResponse,
)
from api.services.telemetry_ingest import produce_telemetry_records

router = APIRouter(prefix='/telemetry', tags=['telemetry'])

TelemetryPayload = dict[str, Any] | list[Any]


@router.post(
    '',
    responses={
        202: {'model': TelemetryAcceptedResponse},
        422: {'model': TelemetryRejectedResponse},
        503: {'model': TelemetryUnavailableResponse},
    },
)
async def ingest_telemetry(
        payload: Annotated[TelemetryPayload, Body(...)],
        producer: KafkaProducer = Depends(get_kafka_producer),
        settings: Settings = Depends(get_settings),
) -> JSONResponse:
    result = produce_telemetry_records(
        payload=payload,
        producer=producer,
        settings=settings,
    )

    return JSONResponse(
        status_code=_map_status_to_http_code(result.status),
        content={
            'status': result.status,
            'accepted': result.accepted,
            'skipped': result.skipped,
            'errors': result.errors,
        },
    )


def _map_status_to_http_code(status: ProduceTelemetryStatus) -> int:
    if status == ProduceTelemetryStatus.ACCEPTED:
        return 202
    if status == ProduceTelemetryStatus.REJECTED:
        return 422
    if status == ProduceTelemetryStatus.UNAVAILABLE:
        return 503
    return 500
