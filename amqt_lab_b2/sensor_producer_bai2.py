import json
import random
import time
import pika


QUEUE_NAME = "sensor_data_queue"
DEVICE_ID = "sensor01"


def main():
    # Kết nối RabbitMQ
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost")
    )
    channel = connection.channel()

    # Tạo queue nếu chưa tồn tại
    channel.queue_declare(
        queue=QUEUE_NAME,
        durable=True
    )

    print("Sensor Producer started...")
    print(f"Sending data to queue: {QUEUE_NAME}")

    try:
        while True:
            # Sinh dữ liệu ngẫu nhiên
            temperature = round(random.uniform(20, 40), 1)
            humidity = round(random.uniform(30, 80), 1)

            # Tạo payload JSON
            data = {
                "device_id": DEVICE_ID,
                "temperature": temperature,
                "humidity": humidity
            }

            message = json.dumps(data)

            # Gửi message vào queue
            channel.basic_publish(
                exchange="",
                routing_key=QUEUE_NAME,
                body=message
            )

            print(f"Sent: {message}")

            # Gửi mỗi 3 giây
            time.sleep(3)

    except KeyboardInterrupt:
        print("\nProducer stopped.")

    finally:
        connection.close()


if __name__ == "__main__":
    main()