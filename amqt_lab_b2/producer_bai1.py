import json
import random
import time
import pika


QUEUE_NAME = "sensor_data_queue"
DEVICE_ID = "sensor01"


def connect_rabbitmq():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost")
    )
    channel = connection.channel()

    # Tạo queue nếu chưa tồn tại
    channel.queue_declare(
        queue=QUEUE_NAME,
        durable=True
    )

    return connection, channel


def main():
    connection, channel = connect_rabbitmq()

    print("Sensor Producer started...")
    print(f"Sending data to queue: {QUEUE_NAME}")

    try:
        while True:
            temperature = round(random.uniform(20, 40), 1)
            humidity = round(random.uniform(30, 80), 1)

            data = {
                "device_id": DEVICE_ID,
                "temperature": temperature,
                "humidity": humidity
            }

            message = json.dumps(data)

            channel.basic_publish(
                exchange="",
                routing_key=QUEUE_NAME,
                body=message,
                properties=pika.BasicProperties(
                    delivery_mode=2
                )
            )

            print(f"Sent: {message}")

            time.sleep(3)

    except KeyboardInterrupt:
        print("\nProducer stopped.")

    finally:
        connection.close()


if __name__ == "__main__":
    main()