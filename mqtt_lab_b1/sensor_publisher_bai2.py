import paho.mqtt.client as mqtt
import json
import random
import time

# MQTT Broker
BROKER = "test.mosquitto.org"
PORT = 1883

# Topic
TOPIC = "iot/lab/sensor01/data"

# Thông tin thiết bị
DEVICE_ID = "sensor01"

# Tạo MQTT Client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

print("Dang ket noi toi MQTT Broker...")

client.connect(BROKER, PORT, 60)

print("Ket noi thanh cong!")
print("Sensor dang gui du lieu moi 3 giay.")
print("Nhan Ctrl+C de dung.\n")

try:
    while True:

        # Sinh nhiet do ngau nhien
        temperature = round(random.uniform(25, 40), 1)

        # Sinh do am ngau nhien
        humidity = round(random.uniform(30, 80), 1)

        # Tao du lieu JSON
        data = {
            "device_id": DEVICE_ID,
            "temperature": temperature,
            "humidity": humidity
        }

        # Chuyen dictionary thanh JSON
        payload = json.dumps(data)

        # Gui message
        result = client.publish(TOPIC, payload)

        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            print("Da gui:")
            print(f"Device: {DEVICE_ID}")
            print(f"Temperature: {temperature} C")
            print(f"Humidity: {humidity} %")
            print("-" * 30)

        # Cho 3 giay
        time.sleep(3)

except KeyboardInterrupt:
    print("\nDang dung Sensor Publisher...")

finally:
    client.disconnect()
    print("Da ngat ket noi.")