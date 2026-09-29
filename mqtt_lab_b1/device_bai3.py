import paho.mqtt.client as mqtt
import json

BROKER = "test.mosquitto.org"
PORT = 1883

CMD_TOPIC = "iot/lab/light01/cmd"
STATUS_TOPIC = "iot/lab/light01/status"

DEVICE_ID = "light01"

# Trạng thái ban đầu
light_status = "OFF"


# Khi kết nối Broker
def on_connect(client, userdata, flags, reason_code, properties):

    if reason_code == 0:
        print("Smart Light da ket noi MQTT Broker.")

        # Subscribe topic điều khiển
        client.subscribe(CMD_TOPIC)

        print(f"Dang cho lenh tai: {CMD_TOPIC}\n")

    else:
        print("Ket noi that bai!")


# Khi nhận được lệnh
def on_message(client, userdata, msg):

    global light_status

    command = msg.payload.decode("utf-8").strip().upper()

    print(f"Nhan lenh: {command}")

    if command == "ON":
        light_status = "ON"

    elif command == "OFF":
        light_status = "OFF"

    else:
        print("Lenh khong hop le!")
        return

    # Tạo JSON trạng thái
    status_data = {
        "device_id": DEVICE_ID,
        "status": light_status
    }

    status_payload = json.dumps(status_data)

    # Gửi trạng thái mới
    client.publish(STATUS_TOPIC, status_payload)

    print(f"Da cap nhat den: {light_status}")
    print(f"Da gui trang thai: {status_payload}")
    print("-" * 40)


# Tạo MQTT Client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

client.on_connect = on_connect
client.on_message = on_message

print("Dang ket noi toi MQTT Broker...")

client.connect(BROKER, PORT, 60)

try:
    client.loop_forever()

except KeyboardInterrupt:
    print("\nDang dung Smart Light...")

finally:
    client.disconnect()
    print("Da ngat ket noi.")