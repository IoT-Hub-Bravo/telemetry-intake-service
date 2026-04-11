from fastapi import Request

from kafka_producers import KafkaProducer


def get_kafka_producer(request: Request) -> KafkaProducer:
    return request.app.state.kafka_producer
