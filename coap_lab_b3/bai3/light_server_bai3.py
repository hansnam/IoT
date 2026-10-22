import argparse
import asyncio
from datetime import datetime
import json
import os
import aiocoap
import aiocoap.resource as resource

class SmartLightResource(resource.ObservableResource):
    """
    Tai nguyen CoAP dieu khien va giam sat den thong minh co ho tro Observe.
    - GET: Tra ve trang thai hien tai (ON/OFF).
    - PUT: Nhan lenh dieu khien (ON/OFF).
    - Observe: Tu dong thong bao cho cac Client theo doi khi trang thai thay doi.
    """
    def __init__(self, device_id: str = "light01", log_file: str = "light_state_history.log"):
        super().__init__()
        self.device_id = device_id
        self.status = "OFF"  # Trang thai ban dau
        self.log_file = log_file

    async def add_observation(self, request, serverobservation):
        now = datetime.now().strftime("%H:%M:%S")
        print(f"[{now}] [{self.device_id}] New Observe registration received", flush=True)
        await super().add_observation(request, serverobservation)

    async def render_get(self, request):
        now = datetime.now().strftime("%H:%M:%S")
        print(f"[{now}] [{self.device_id}] GET request received", flush=True)

        payload_dict = {
            "device_id": self.device_id,
            "status": self.status,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        payload_bytes = json.dumps(payload_dict, indent=2).encode("utf-8")

        return aiocoap.Message(
            code=aiocoap.CONTENT,
            payload=payload_bytes,
            content_format=aiocoap.ContentFormat.JSON
        )

    async def render_put(self, request):
        now = datetime.now().strftime("%H:%M:%S")
        payload_raw = request.payload.decode("utf-8", errors="replace")

        try:
            body = json.loads(payload_raw)
        except Exception:
            # Ho tro ca chuoi plaintext ON/OFF truc tiep
            body = {"command": payload_raw.strip()}

        command = str(body.get("command", "")).strip().upper()
        target_device = body.get("device_id", self.device_id)

        print(f"[{now}] PUT request received:", flush=True)
        print(f"  Device: {target_device}", flush=True)
        print(f"  Command: {command}", flush=True)

        # Kiem tra lenh hop le (ON hoac OFF)
        if command not in ["ON", "OFF"]:
            err_payload = json.dumps({
                "error": "Lenh khong hop le. Chi chap nhan ON hoac OFF.",
                "received": command
            }).encode("utf-8")
            print(f"[{now}] Rejected invalid command: {command}", flush=True)
            return aiocoap.Message(
                code=aiocoap.BAD_REQUEST,
                payload=err_payload,
                content_format=aiocoap.ContentFormat.JSON
            )

        old_state = self.status
        state_changed = (old_state != command)

        if state_changed:
            self.status = command
            print(f"  Light state changed: {old_state} -> {self.status}", flush=True)
            print(f"  Notify observers: {self.status}", flush=True)

            # Ghi nhat ky thay doi ra file
            try:
                log_entry = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {self.device_id}: {old_state} -> {self.status}\n"
                with open(self.log_file, "a", encoding="utf-8") as f:
                    f.write(log_entry)
            except Exception as e:
                print(f"Khong the ghi log: {e}", flush=True)

            # Kich hoat thong bao Observe den tat ca cac Client dang theo doi
            self.updated_state()
        else:
            print(f"  Light state unchanged: {self.status}", flush=True)

        response_dict = {
            "device_id": self.device_id,
            "status": self.status,
            "message": f"Da cap nhat trang thai thanh {self.status}"
        }
        return aiocoap.Message(
            code=aiocoap.CHANGED,
            payload=json.dumps(response_dict, indent=2).encode("utf-8"),
            content_format=aiocoap.ContentFormat.JSON
        )

async def start_server(host: str, port: int):
    root = resource.Site()

    # Thiet bi chinh light01
    light1 = SmartLightResource("light01")
    root.add_resource(["iot", "lab", "light01", "status"], light1)

    # Thiet bi mo rong fan01 (quat thong minh)
    fan1 = SmartLightResource("fan01")
    root.add_resource(["iot", "lab", "fan01", "status"], fan1)

    server = await aiocoap.Context.create_server_context(root, bind=(host, port))

    print("=" * 65, flush=True)
    print("CoAP Smart Light Server started...")
    print(f"Resource: /iot/lab/light01/status (URI: coap://{host}:{port}/iot/lab/light01/status)", flush=True)
    print(f"Resource: /iot/lab/fan01/status   (Mo rong: Quat thong minh)", flush=True)
    print(f"Initial state: light01 = OFF", flush=True)
    print("Supports: GET (xem trang thai), PUT (bat/tat), Observe (nhan thong bao tu dong)", flush=True)
    print("Dang cho yeu cau... (Nhan Ctrl+C de dung)", flush=True)
    print("=" * 65, flush=True)

    try:
        await asyncio.get_running_loop().create_future()
    except asyncio.CancelledError:
        pass
    finally:
        print("\nDang dung Smart Light Server...", flush=True)
        await server.shutdown()
        print("Smart Light Server da dong.", flush=True)

def main():
    parser = argparse.ArgumentParser(description="Smart Light CoAP Server - Bai 3")
    parser.add_argument("--host", default="127.0.0.1", help="Dia chi IP bind (mac dinh: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=5683, help="Cong CoAP (mac dinh: 5683)")
    args = parser.parse_args()

    try:
        asyncio.run(start_server(args.host, args.port))
    except KeyboardInterrupt:
        print("\nDa nhan tin hieu KeyboardInterrupt. Thoat chuong trinh.", flush=True)

if __name__ == "__main__":
    main()
