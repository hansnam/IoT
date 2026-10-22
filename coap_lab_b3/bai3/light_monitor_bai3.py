import argparse
import asyncio
from datetime import datetime
import json
import sys
import aiocoap

async def run_observe_monitor(host: str, port: int, device_id: str):
    uri = f"coap://{host}:{port}/iot/lab/{device_id}/status"

    print("=" * 60, flush=True)
    print("Light Monitoring Client (CoAP Observe)")
    print(f"Target Resource URI: {uri}")
    print("Dang ket noi va dang ky CoAP Observe...")
    print("=" * 60, flush=True)

    try:
        client = await aiocoap.Context.create_client_context()
    except Exception as e:
        print(f"Loi khoi tao CoAP Context: {e}", flush=True)
        return

    # Dang ky Observe: request GET voi option observe=0
    print("Registering CoAP Observe...", flush=True)
    request = aiocoap.Message(code=aiocoap.GET, uri=uri, observe=0)
    pr = client.request(request)

    try:
        # Nhan phan hoi ban dau
        initial_response = await asyncio.wait_for(pr.response, timeout=5.0)
        print("Observe registration successful", flush=True)

        initial_payload = initial_response.payload.decode("utf-8", errors="replace")
        try:
            data = json.loads(initial_payload)
            dev = data.get("device_id", device_id)
            status = data.get("status", "UNKNOWN")
        except Exception:
            dev = device_id
            status = initial_payload.strip()

        now_str = datetime.now().strftime("%H:%M:%S")
        print(f"[{now_str}] Initial State", flush=True)
        print(f"Device: {dev}", flush=True)
        print(f"Status: {status}", flush=True)
        print("-" * 35, flush=True)

        # Lang nghe cac thong bao cap nhat qua CoAP Observe stream
        # LUU Y: Day la CoAP Observe push notification tu server, KHONG phai GET dinh ky!
        async for notification in pr.observation:
            notif_payload = notification.payload.decode("utf-8", errors="replace")
            now_str = datetime.now().strftime("%H:%M:%S")
            try:
                data = json.loads(notif_payload)
                dev = data.get("device_id", device_id)
                status = data.get("status", "UNKNOWN")
            except Exception:
                dev = device_id
                status = notif_payload.strip()

            print(f"[{now_str}] State Updated", flush=True)
            print(f"Device: {dev}", flush=True)
            print(f"Status: {status}", flush=True)
            print("-" * 35, flush=True)

    except asyncio.TimeoutError:
        print("Loi: Khong nhan duoc phan hoi dang ky Observe tu Server (Timeout)!", flush=True)
    except asyncio.CancelledError:
        pass
    except Exception as e:
        print(f"Loi trong qua trinh Observe: {e}", flush=True)
    finally:
        print("\nHuy dang ky CoAP Observe...", flush=True)
        try:
            if hasattr(pr, "observation") and pr.observation:
                pr.observation.cancel()
        except Exception:
            pass
        await client.shutdown()
        print("Da dong ket noi Monitoring Client.", flush=True)

def main():
    parser = argparse.ArgumentParser(description="Light Monitoring Client (CoAP Observe) - Bai 3")
    parser.add_argument("--host", default="127.0.0.1", help="Dia chi CoAP Server (mac dinh: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=5683, help="Cong CoAP (mac dinh: 5683)")
    parser.add_argument("--device", default="light01", help="Ma thiet bi (mac dinh: light01)")
    args = parser.parse_args()

    try:
        asyncio.run(run_observe_monitor(args.host, args.port, args.device))
    except KeyboardInterrupt:
        print("\nDa nhan tin hieu KeyboardInterrupt. Thoat chuong trinh.", flush=True)

if __name__ == "__main__":
    main()
