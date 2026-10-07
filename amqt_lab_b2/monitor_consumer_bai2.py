import json
import pika


QUEUE_NAME = "sensor_data_queue"


def callback(ch, method, properties, body):
    # Chuyển JSON thành dictionary
    data = json.loads(body.decode("utf-8"))

    device_id = data["device_id"]
    temperature = data["temperature"]
    humidity = data["humidity"]

    print("\n-----------------------------")
    print(f"Device: {device_id}")
    print(f"Temperature: {temperature}")
    print(f"Humidity: {humidity}")

    # Kiểm tra cảnh báo nhiệt độ
    if temperature > 35:
        print("CANH BAO: Nhiet do cao")

    # Kiểm tra cảnh báo độ ẩm
    if humidity < 40:
        print("CANH BAO: Do am thap")

    # Xác nhận message đã xử lý
    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    # Kết nối RabbitMQ
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost")
    )
    channel = connection.channel()

    # Đảm bảo queue tồn tại
    channel.queue_declare(
        queue=QUEUE_NAME,
        durable=True
    )

    # Đăng ký consumer
    channel.basic_consume(
        queue=QUEUE_NAME,
        on_message_callback=callback,
        auto_ack=False
    )

    print("Monitoring Consumer started...")
    print(f"Waiting for messages from: {QUEUE_NAME}")

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("\nConsumer stopped.")
        channel.stop_consuming()
    finally:
        connection.close()


if __name__ == "__main__":
    main()