import json
import pika


QUEUE_NAME = "sensor_data_queue"


def callback(ch, method, properties, body):
    try:
        # Chuyển JSON string -> Python dictionary
        data = json.loads(body.decode("utf-8"))

        device_id = data["device_id"]
        temperature = data["temperature"]
        humidity = data["humidity"]

        print("\n-----------------------------")
        print(f"Device: {device_id}")
        print(f"Temperature: {temperature}")
        print(f"Humidity: {humidity}")

        # Kiểm tra nhiệt độ
        if temperature > 35:
            print("CANH BAO: Nhiet do cao")

        # Kiểm tra độ ẩm
        if humidity < 40:
            print("CANH BAO: Do am thap")

        # Xác nhận đã xử lý message
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except (json.JSONDecodeError, KeyError, TypeError) as e:
        print(f"Loi xu ly message: {e}")

        # Message lỗi vẫn xác nhận để tránh xử lý vô hạn
        ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost")
    )

    channel = connection.channel()

    channel.queue_declare(
        queue=QUEUE_NAME,
        durable=True
    )

    # Mỗi consumer nhận từng message
    channel.basic_qos(prefetch_count=1)

    channel.basic_consume(
        queue=QUEUE_NAME,
        on_message_callback=callback
    )

    print("Monitoring Consumer started...")
    print(f"Waiting for messages from: {QUEUE_NAME}")
    print("Press Ctrl+C to stop.")

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("\nConsumer stopped.")
        channel.stop_consuming()
    finally:
        connection.close()


if __name__ == "__main__":
    main()