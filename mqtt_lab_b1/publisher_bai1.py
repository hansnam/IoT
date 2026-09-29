import paho.mqtt.client as mqtt
import time

BROKER = "test.mosquitto.org"
PORT = 1883

TOPIC = "iot/lab/message"

NAME = "Tran Han Nam"
STUDENT_ID = "B23DCCN590"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

print("Dang ket noi toi MQTT Broker ...")

client.connect(BROKER, 1883, 60)

print("Ket noi thanh cong")
i = 0

try:
    while True:
        i = i + 1
        message = (
            f"Xin chao tu client Python MQTT - "
            f"{STUDENT_ID} - {NAME} - Message {i}"
        )

        result = client.publish(TOPIC, message)

        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            print(f"Da gui: {message}")
        else:
            print("Gui message that bai!")

        time.sleep(2)

except KeyboardInterrupt:
    print("\nDung publisher...")

finally:
    client.disconnect()
    print("Da ngat ket noi.")