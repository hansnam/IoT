import argparse
import asyncio
from datetime import datetime
import json
import random
import aiocoap
import aiocoap.resource as resource

class SensorDataResource(resource.Resource):
    """
    Tai nguyen CoAP bieu dien cam bien nhiet do va do am.
    Cung cap:
    - GET: Tra ve du lieu JSON voi device_id, temperature, humidity, timestamp.
    - Content-Format: application/json
    """
    def __init__(self, device_id: str = "sensor01", update_interval: float = 3.0):
        super().__init__()
        self.device_id = device_id
        self.update_interval = update_interval
        
        # Gia tri khoi tao
        self.temperature = round(random.uniform(25.0, 32.0), 1)
        self.humidity = round(random.uniform(50.0, 70.0), 1)
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def update_sensor_reading(self):
        """
        Cap nhat gia tri cam bien voi su thay doi ngau nhien hop ly.
        Co xac suat tao ra nhiet do > 35 do C va do am < 40% de test canh bao.
        """
        # 25% co hoi roi vao vung bat thuong (nhiet do cao hoac do am thap)
        scenario = random.random()
        if scenario < 0.15:
            # Nhiet do cao
            self.temperature = round(random.uniform(35.5, 41.0), 1)
            self.humidity = round(random.uniform(40.0, 60.0), 1)
        elif scenario < 0.30:
            # Do am thap
            self.temperature = round(random.uniform(28.0, 34.0), 1)
            self.humidity = round(random.uniform(30.0, 39.5), 1)
        elif scenario < 0.40:
            # Ca hai canh bao
            self.temperature = round(random.uniform(35.5, 40.0), 1)
            self.humidity = round(random.uniform(30.0, 39.0), 1)
        else:
            # Binh thuong
            self.temperature = round(random.uniform(24.0, 34.0), 1)
            self.humidity = round(random.uniform(45.0, 75.0), 1)

        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    async def background_update_loop(self):
        """
        Cap nhat du lieu cam bien dinh ky moi update_interval giay.
        """
        while True:
            await asyncio.sleep(self.update_interval)
            self.update_sensor_reading()
            now_time = datetime.now().strftime("%H:%M:%S")
            print(f"[{now_time}] [{self.device_id}] Data updated -> Temp: {self.temperature} C, Hum: {self.humidity}%", flush=True)

    async def render_get(self, request):
        now_time = datetime.now().strftime("%H:%M:%S")
        print(f"[{now_time}] [{self.device_id}] GET request received from Client", flush=True)

        payload_dict = {
            "device_id": self.device_id,
            "temperature": self.temperature,
            "humidity": self.humidity,
            "timestamp": self.timestamp
        }
        payload_bytes = json.dumps(payload_dict, indent=2).encode("utf-8")

        return aiocoap.Message(
            code=aiocoap.CONTENT,
            payload=payload_bytes,
            content_format=aiocoap.ContentFormat.JSON
        )

async def start_server(host: str, port: int, interval: float):
    root = resource.Site()

    # Khoi tao sensor01 (chinh theo de bai) va sensor02, sensor03 (mo rong)
    sensor1 = SensorDataResource("sensor01", interval)
    sensor2 = SensorDataResource("sensor02", interval)
    sensor3 = SensorDataResource("sensor03", interval)

    root.add_resource(["iot", "lab", "sensor01", "data"], sensor1)
    root.add_resource(["iot", "lab", "sensor02", "data"], sensor2)
    root.add_resource(["iot", "lab", "sensor03", "data"], sensor3)

    server = await aiocoap.Context.create_server_context(root, bind=(host, port))

    print("=" * 65, flush=True)
    print(f"Sensor CoAP Server started on {host}:{port}", flush=True)
    print("Available resources:", flush=True)
    print(f"  - coap://{host}:{port}/iot/lab/sensor01/data (Chinh)", flush=True)
    print(f"  - coap://{host}:{port}/iot/lab/sensor02/data (Mo rong)", flush=True)
    print(f"  - coap://{host}:{port}/iot/lab/sensor03/data (Mo rong)", flush=True)
    print(f"Update interval: {interval} seconds", flush=True)
    print("Content-Format: application/json (50)", flush=True)
    print("Dang phuc vu yeu cau GET... (Nhan Ctrl+C de dung)", flush=True)
    print("=" * 65, flush=True)

    # Chay cac task cap nhat ngam
    tasks = [
        asyncio.create_task(sensor1.background_update_loop()),
        asyncio.create_task(sensor2.background_update_loop()),
        asyncio.create_task(sensor3.background_update_loop()),
    ]

    try:
        await asyncio.gather(*tasks)
    except asyncio.CancelledError:
        pass
    finally:
        print("\nDang dung Sensor CoAP Server...", flush=True)
        for t in tasks:
            t.cancel()
        await server.shutdown()
        print("Sensor CoAP Server da dong.", flush=True)

def main():
    parser = argparse.ArgumentParser(description="Sensor CoAP Server - Bai 2")
    parser.add_argument("--host", default="127.0.0.1", help="Dia chi IP bind (mac dinh: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=5683, help="Cong CoAP (mac dinh: 5683)")
    parser.add_argument("--interval", type=float, default=3.0, help="Chu ky cap nhat cam bien giay (mac dinh: 3.0)")
    args = parser.parse_args()

    try:
        asyncio.run(start_server(args.host, args.port, args.interval))
    except KeyboardInterrupt:
        print("\nDa nhan tin hieu KeyboardInterrupt. Thoat chuong trinh.", flush=True)

if __name__ == "__main__":
    main()
