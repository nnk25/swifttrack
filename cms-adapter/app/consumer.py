import asyncio
from aio_pika import connect_robust, ExchangeType
from aio_pika.abc import AbstractIncomingMessage
from os import getenv

async def consume_event():
    connection = await connect_robust(getenv("RABBITMQ_URL"))
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=1)

    exchange = await channel.declare_exchange("swifttrack.events", ExchangeType.TOPIC, durable=True)
    queue = await channel.declare_queue("orders_queue", durable = True)
    await queue.bind(exchange, routing_key="orders.*")
    print("Running")

    async with queue.iterator() as iterator:
        message: AbstractIncomingMessage
        async for message in iterator:
            async with message.process():
                print(f" [x] {message.routing_key!r}:{message.body!r}")

# if __name__ == "__main__":
#     asyncio.run(consume_event())