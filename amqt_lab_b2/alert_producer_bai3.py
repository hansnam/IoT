import pika


EXCHANGE_NAME = "iot_alert_exchange"


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

    alerts = [
        ("info", "Nhiet do phong may chuot muc info"),
        ("warning", "Nhiet do phong may vuot nguong warning"),
        ("critical", "Cam bien kho lanh mat ket noi critical")
    ]

    for routing_key, message in alerts:
        channel.basic_publish(
            exchange=EXCHANGE_NAME,
            routing_key=routing_key,
            body=message
        )

        print(f"[Producer] Da gui ({routing_key}): {message}")

    connection.close()


if __name__ == "__main__":
    main()