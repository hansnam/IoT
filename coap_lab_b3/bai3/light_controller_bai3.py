import argparse
import asyncio
from datetime import datetime
import json
import sys
import aiocoap

async def execute_command(client, uri: str, device_id: str, cmd_input: str) -> bool:
    """
    Xu ly mot lenh dieu khien hoac truy van.
    Tra ve True de tiep tuc, False neu muon thoat.
    """
    cmd = cmd_input.strip().upper()

    if not cmd:
        return True

    if cmd == "EXIT":
        print("Ket thuc chuong trinh Light Controller.")
        return False

    if cmd in ["ON", "OFF"]:
        print("Sending PUT request...", flush=True)
        payload_dict = {
            "device_id": device_id,
            "command": cmd
        }
        payload_bytes = json.dumps(payload_dict).encode("utf-8")

        req = aiocoap.Message(
            code=aiocoap.PUT,
            uri=uri,
            payload=payload_bytes,
            content_format=aiocoap.ContentFormat.JSON
        )

        try:
            resp = await asyncio.wait_for(client.request(req).response, timeout=5.0)
            print(f"Response Code: {resp.code}", flush=True)
            if resp.code.is_successful():
                if cmd == "ON":
                    print(f"Da bat den {device_id}", flush=True)
                else:
                    print(f"Da tat den {device_id}", flush=True)
            else:
                print(f"Phan hoi loi tu server: {resp.payload.decode('utf-8', errors='replace')}", flush=True)
        except asyncio.TimeoutError:
            print("Loi: Yeu cau PUT het thoi gian cho (Timeout)! Kiem tra Server.", flush=True)
        except Exception as e:
            print(f"Loi khi gui PUT: {e}", flush=True)

    elif cmd == "STATUS":
        print("Sending GET request...", flush=True)
        req = aiocoap.Message(code=aiocoap.GET, uri=uri)

        try:
            resp = await asyncio.wait_for(client.request(req).response, timeout=5.0)
            print(f"Response Code: {resp.code}", flush=True)
            print("Response:", flush=True)
            print(resp.payload.decode("utf-8", errors="replace"), flush=True)
        except asyncio.TimeoutError:
            print("Loi: Yeu cau GET het thoi gian cho (Timeout)! Kiem tra Server.", flush=True)
        except Exception as e:
            print(f"Loi khi gui GET: {e}", flush=True)

    else:
        print("Lenh khong hop le! Vui long nhap ON, OFF, STATUS hoac EXIT.", flush=True)

    return True

async def run_controller(host: str, port: int, device_id: str, one_shot_cmd: str = None):
    uri = f"coap://{host}:{port}/iot/lab/{device_id}/status"

    try:
        client = await aiocoap.Context.create_client_context()
    except Exception as e:
        print(f"Loi khoi tao CoAP Client: {e}", flush=True)
        return

    print("=" * 60, flush=True)
    print(f"Light Controller Client connected")
    print(f"Target Resource URI: {uri}")
    print(f"Target Device: {device_id}")
    print("=" * 60, flush=True)

    try:
        if one_shot_cmd:
            await execute_command(client, uri, device_id, one_shot_cmd)
            return

        while True:
            # Dung asyncio.to_thread de khong chan event loop khi doi input tu ban phim
            user_input = await asyncio.to_thread(input, "\nNhap lenh (ON/OFF/STATUS/EXIT): ")
            keep_running = await execute_command(client, uri, device_id, user_input)
            if not keep_running:
                break

    finally:
        await client.shutdown()
        print("Da ngat ket noi Controller Client.", flush=True)

def main():
    parser = argparse.ArgumentParser(description="Light Controller Client - Bai 3")
    parser.add_argument("--host", default="127.0.0.1", help="Dia chi CoAP Server (mac dinh: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=5683, help="Cong CoAP (mac dinh: 5683)")
    parser.add_argument("--device", default="light01", help="Ma thiet bi (mac dinh: light01)")
    parser.add_argument("--cmd", default=None, help="Gui nhanh mot lenh (ON, OFF, STATUS) roi thoat")
    args = parser.parse_args()

    try:
        asyncio.run(run_controller(args.host, args.port, args.device, args.cmd))
    except KeyboardInterrupt:
        print("\nDa nhan tin hieu KeyboardInterrupt. Thoat Controller.", flush=True)

if __name__ == "__main__":
    main()
