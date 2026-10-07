import pika


EXCHANGE_NAME = "iot_alert_exchange"
QUEUE_NAME = "critical_queue"
ROUTING_KEY = "critical"


def callback(ch, method, properties, body):
    message = body.decode("utf-8")

    print(f"[critical_queue] Da nhan: {message}")

    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost")
    )
    channel = connection.channel()

    # Tạo direct exchange
    channel.exchange_declare(
        exchange=EXCHANGE_NAME,
        exchange_type="direct",
        durable=True
    )

    # Tạo queue
    channel.queue_declare(
        queue=QUEUE_NAME,
        durable=True
    )

    # Bind queue với routing key critical
    channel.queue_bind(
        exchange=EXCHANGE_NAME,
        queue=QUEUE_NAME,
        routing_key=ROUTING_KEY
    )

    channel.basic_consume(
        queue=QUEUE_NAME,
        on_message_callback=callback,
        auto_ack=False
    )

    print("[Critical Consumer] Dang cho canh bao critical...")

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("\nCritical Consumer stopped.")
        channel.stop_consuming()
    finally:
        connection.close()


if __name__ == "__main__":
    main()