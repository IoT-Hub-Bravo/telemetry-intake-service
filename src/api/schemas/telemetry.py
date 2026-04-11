from pydantic import BaseModel, Field

from api.domain.telemetry import ProduceTelemetryStatus


class BaseTelemetryResponse(BaseModel):
    status: ProduceTelemetryStatus
    accepted: int
    skipped: int
    errors: dict[str | int, str] = Field(default_factory=dict)


class TelemetryAcceptedResponse(BaseTelemetryResponse):
    status: ProduceTelemetryStatus = ProduceTelemetryStatus.ACCEPTED


class TelemetryRejectedResponse(BaseTelemetryResponse):
    status: ProduceTelemetryStatus = ProduceTelemetryStatus.REJECTED
    accepted: int = 0


class TelemetryUnavailableResponse(BaseTelemetryResponse):
    status: ProduceTelemetryStatus = ProduceTelemetryStatus.UNAVAILABLE
    accepted: int = 0
