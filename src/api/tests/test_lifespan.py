from unittest.mock import Mock, patch

from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.core.lifespan import lifespan


@patch('api.core.lifespan.get_telemetry_raw_producer')
def test_lifespan_sets_kafka_producer_on_startup(mock_get_producer):
    """Test lifespan stores producer in app state on startup."""
    producer = Mock()
    mock_get_producer.return_value = producer

    app = FastAPI(lifespan=lifespan)

    with TestClient(app) as client:
        assert client.app.state.kafka_producer is producer


@patch('api.core.lifespan.get_telemetry_raw_producer')
def test_lifespan_flushes_producer_on_shutdown(mock_get_producer):
    """Test lifespan flushes producer on shutdown."""
    producer = Mock()
    mock_get_producer.return_value = producer

    app = FastAPI(lifespan=lifespan)

    with TestClient(app):
        pass

    producer.flush.assert_called_once()
