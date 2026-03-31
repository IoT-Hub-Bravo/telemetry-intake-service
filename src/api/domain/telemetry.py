from dataclasses import dataclass, field
from enum import Enum


class ProduceTelemetryStatus(str, Enum):
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'
    UNAVAILABLE = 'unavailable'


@dataclass(slots=True, frozen=True)
class ProduceTelemetryResult:
    status: ProduceTelemetryStatus
    accepted: int = 0
    skipped: int = 0
    errors: dict[str | int, str] = field(default_factory=dict)
