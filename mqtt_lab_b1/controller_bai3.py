import paho.mqtt.client as mqtt
import time

BROKER = "test.mosquitto.org"
PORT = 1883

CMD_TOPIC = "iot/lab/light01/cmd"
STATUS_TOPIC = "iot/lab/light01/status"


# Khi kết nối Broker
def on_connect(client, userdata, flags, reason_code, properties):

    if reason_code == 0:
        print("Controller da ket noi MQTT Broker.")

        # Subscribe trạng thái
        client.subscribe(STATUS_TOPIC)

        print(f"Dang lang nghe: {STATUS_TOPIC}\n")

    else:
        print("Ket noi that bai!")


# Khi nhận trạng thái từ Smart Light
def on_message(client, userdata, msg):

    status = msg.payload.decode("utf-8")

    print("\nTrang thai nhan duoc:")
    print(status)
    print()


# Tạo MQTT Client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

client.on_connect = on_connect
client.on_message = on_message

print("Dang ket noi toi MQTT Broker...")

client.connect(BROKER, PORT, 60)

# Chạy MQTT network loop ở background
client.loop_start()

try:

    while True:

        command = input("Nhap lenh (ON/OFF/EXIT): ").strip().upper()

        if command == "EXIT":
            print("Dang thoat Controller...")
            break

        if command not in ["ON", "OFF"]:
            print("Lenh khong hop le! Chi duoc nhap ON, OFF hoac EXIT.\n")
            continue

        # Gửi lệnh
        client.publish(CMD_TOPIC, command)

        print(f"Da gui lenh {command} toi light01")

        # Cho Smart Light xử lý và trả trạng thái
        time.sleep(0.5)

except KeyboardInterrupt:
    print("\nDang dung Controller...")

finally:
    client.loop_stop()
    client.disconnect()
    print("Da ngat ket noi.")