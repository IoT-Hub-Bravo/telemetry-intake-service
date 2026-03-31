from functools import lru_cache
from decouple import config


class Settings:
    app_name: str = config('APP_NAME', default='telemetry-intake-service')
    app_version: str = config('APP_VERSION', default='0.1.0')
    debug: bool = config('DEBUG', default=False, cast=bool)
    api_prefix: str = config('API_PREFIX', default='/api')
    http_producer_key_field: str = config('HTTP_PRODUCER_KEY_FIELD', default='device_serial_id')


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
