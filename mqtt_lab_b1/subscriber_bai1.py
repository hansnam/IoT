import paho.mqtt.client as mqtt
from datetime import datetime

# MQTT Broker
BROKER = "test.mosquitto.org"
PORT = 1883

# Topic cần lắng nghe
TOPIC = "iot/lab/message"


# Hàm được gọi khi kết nối tới Broker thành công
def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Ket noi MQTT Broker thanh cong!")
        
        # Đăng ký topic
        client.subscribe(TOPIC)
        
        print(f"Dang lang nghe topic: {TOPIC}")
        print("Cho message...\n")
    else:
        print(f"Ket noi that bai. Ma loi: {reason_code}")


# Hàm được gọi khi nhận được message
def on_message(client, userdata, msg):
    # Lấy thời điểm hiện tại
    current_time = datetime.now().strftime("%H:%M:%S")

    # Chuyển payload từ bytes sang string
    payload = msg.payload.decode("utf-8")

    print("Nhan duoc message:")
    print(f"Topic: {msg.topic}")
    print(f"Payload: {payload}")
    print(f"Time: {current_time}")
    print("-" * 40)


# Tạo MQTT Client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

# Đăng ký callback
client.on_connect = on_connect
client.on_message = on_message

# Kết nối Broker
print("Dang ket noi toi MQTT Broker...")

client.connect(BROKER, PORT, 60)

# Chạy liên tục để nhận message
try:
    client.loop_forever()

except KeyboardInterrupt:
    print("\nDang ngat ket noi...")

    client.disconnect()

    print("Da ngat ket noi MQTT Broker.")