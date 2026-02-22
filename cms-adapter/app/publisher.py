import aio_pika
import json
from os import getenv

async def publish_event(routing_key: str, payload: dict):
    connection = await aio_pika.connect_robust(getenv("RABBITMQ_URL"))
    channel = await connection.channel()

    exchange = await channel.declare_exchange(
        "swifttrack.events",
        aio_pika.ExchangeType.TOPIC,
        durable=True
    )

    message = aio_pika.Message(
        body=json.dumps(payload).encode(),
        delivery_mode=aio_pika.DeliveryMode.PERSISTENT
    )

    await exchange.publish(message, routing_key=routing_key)
    await connection.close()