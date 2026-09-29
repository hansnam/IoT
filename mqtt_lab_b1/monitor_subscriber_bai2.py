import paho.mqtt.client as mqtt
import json

# MQTT Broker
BROKER = "test.mosquitto.org"
PORT = 1883

# Topic
TOPIC = "iot/lab/sensor01/data"


# Khi kết nối thành công
def on_connect(client, userdata, flags, reason_code, properties):

    if reason_code == 0:
        print("Ket noi MQTT Broker thanh cong!")

        # Subscribe topic
        client.subscribe(TOPIC)

        print(f"Dang lang nghe: {TOPIC}")
        print("Cho du lieu sensor...\n")

    else:
        print(f"Ket noi that bai: {reason_code}")


# Khi nhận message
def on_message(client, userdata, msg):

    try:
        # Chuyển JSON string thành Python dictionary
        data = json.loads(msg.payload.decode("utf-8"))

        device_id = data["device_id"]
        temperature = data["temperature"]
        humidity = data["humidity"]

        print(f"Device: {device_id}")
        print(f"Temperature: {temperature} C")
        print(f"Humidity: {humidity} %")

        # Kiểm tra nhiệt độ
        if temperature > 35:
            print("CANH BAO: Nhiet do cao")

        # Kiểm tra độ ẩm
        if humidity < 40:
            print("CANH BAO: Do am thap")

        print("-" * 30)

    except json.JSONDecodeError:
        print("Du lieu JSON khong hop le!")

    except KeyError as e:
        print(f"Thieu truong du lieu: {e}")


# Tạo MQTT Client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

# Đăng ký callback
client.on_connect = on_connect
client.on_message = on_message

print("Dang ket noi toi MQTT Broker...")

client.connect(BROKER, PORT, 60)

# Chạy liên tục
try:
    client.loop_forever()

except KeyboardInterrupt:
    print("\nDang dung Monitoring Subscriber...")

finally:
    client.disconnect()
    print("Da ngat ket noi.")