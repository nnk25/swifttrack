import asyncio
import json
import logging
import aio_pika
from app.core.config import settings

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

QUEUE_NAME = "cms.order.created.queue"


def simulate_soap_call(order_id: str) -> dict:
    """Mock SOAP integration. Fails if order_id ends with '999'."""
    if order_id.endswith("999"):
        logger.warning(f"SOAP call FAILED for order {order_id} (simulated failure)")
        return {"success": False, "reason": "CMS rejected order (simulated)"}
    logger.info(f"SOAP call SUCCESS for order {order_id}")
    return {"success": True}


async def handle_message(message: aio_pika.IncomingMessage, exchange: aio_pika.Exchange):
    async with message.process():
        try:
            body = json.loads(message.body)
            order_id = body.get("order_id")
            logger.info(f"CMS Adapter received order.created for order {order_id}")

            result = simulate_soap_call(order_id)

            event_body = {
                "order_id": order_id,
                "failed": not result["success"],
            }
            if not result["success"]:
                event_body["reason"] = result.get("reason")

            out_msg = aio_pika.Message(
                body=json.dumps(event_body).encode(),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                content_type="application/json",
            )
            await exchange.publish(out_msg, routing_key="cms.confirmed")
            logger.info(f"Published cms.confirmed for order {order_id} | failed={event_body['failed']}")

        except Exception as e:
            logger.error(f"CMS Adapter error: {e}", exc_info=True)


async def main():
    await asyncio.sleep(5)  
    logger.info("CMS Adapter connecting to RabbitMQ...")
    connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=10)

    exchange = await channel.declare_exchange(
        settings.EXCHANGE_NAME,
        aio_pika.ExchangeType.TOPIC,
        durable=True,
    )

    queue = await channel.declare_queue(QUEUE_NAME, durable=True)
    await queue.bind(exchange, routing_key="order.created")
    await queue.consume(lambda msg: handle_message(msg, exchange))

    logger.info(f"CMS Adapter listening on {QUEUE_NAME}")
    await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
