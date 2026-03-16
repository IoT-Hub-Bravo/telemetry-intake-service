# IoT Hub Telemetry Intake Service

Telemetry intake service for receiving device data over HTTP and MQTT and publishing it to Kafka.

## Purpose

The Telemetry Intake Service is the single entry point for raw telemetry entering the platform.

## Responsibilities

- receive telemetry over HTTP
- receive telemetry over MQTT
- normalize incoming payloads to the internal message format
- publish raw telemetry to Kafka
- expose ingestion-level observability and health endpoints

## Owned data

This service does not own business data storage.  
It may keep only minimal technical state, logs, or connection metadata.

## Integrations

### Inbound
- IoT devices
- HTTP clients
- MQTT publishers

### Outbound
- Kafka topic for raw telemetry messages

## Technology

- Python
- FastAPI
- Paho
- Kafka
- Docker
