from contextlib import asynccontextmanager

from fastapi import FastAPI

from kafka_producers import get_telemetry_raw_producer


@asynccontextmanager
async def lifespan(app: FastAPI):
    producer = get_telemetry_raw_producer()
    app.state.kafka_producer = producer

    try:
        yield
    finally:
        producer.flush()
