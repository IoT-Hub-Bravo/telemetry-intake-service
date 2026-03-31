from unittest.mock import create_autospec

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from iot_hub_shared.kafka_kit import KafkaProducer

from api.core.settings import Settings, get_settings
from api.dependencies import get_kafka_producer
from api.routers.telemetry import router


@pytest.fixture
def settings():
    settings = create_autospec(Settings, instance=True)
    settings.http_producer_key_field = 'device_serial_id'
    return settings


@pytest.fixture
def producer():
    return create_autospec(KafkaProducer, instance=True)


@pytest.fixture
def app(producer, settings):
    app = FastAPI()
    app.include_router(router)

    app.dependency_overrides[get_kafka_producer] = lambda: producer
    app.dependency_overrides[get_settings] = lambda: settings

    yield app

    app.dependency_overrides.clear()


@pytest.fixture
def client(app):
    with TestClient(app) as client:
        yield client
