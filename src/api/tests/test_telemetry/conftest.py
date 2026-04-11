import pytest


@pytest.fixture
def valid_telemetry_record():
    return {
        'device_serial_id': 'SN-001',
        'metrics': [
            {
                'name': 'temperature',
                'unit': 'celsius',
                'value': 17,
            }
        ],
        'ts': '2026-03-31T11:00:00Z',
    }
