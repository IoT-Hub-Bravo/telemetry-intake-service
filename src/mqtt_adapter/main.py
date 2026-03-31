import signal
import logging

from decouple import config

from kafka_producers import get_telemetry_raw_producer
from mqtt_adapter.config import MqttConfig
from mqtt_adapter.mqtt_client import get_mqtt_client
from mqtt_adapter.message_handlers import KafkaProducerMessageHandler

TOPIC = config('KAFKA_TOPIC_TELEMETRY_RAW', default='telemetry.raw')
KEY_FIELD = config('MQTT_PRODUCER_KEY_FIELD', default='device_serial_id')


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)s %(name)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        force=True,
    )
    logging.getLogger().setLevel(logging.INFO)


def main() -> None:
    setup_logging()
    kafka_producer = get_telemetry_raw_producer()

    message_handler = KafkaProducerMessageHandler(
        producer=kafka_producer,
        key_field=KEY_FIELD,
    )

    client = get_mqtt_client(
        config=MqttConfig(),
        handler=message_handler,
    )

    def _stop(*_):
        client.disconnect()
        kafka_producer.flush()

    signal.signal(signal.SIGTERM, _stop)
    signal.signal(signal.SIGINT, _stop)

    client.loop_forever(retry_first_connection=True)


if __name__ == '__main__':
    main()
