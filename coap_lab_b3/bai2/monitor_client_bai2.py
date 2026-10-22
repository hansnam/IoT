import argparse
import asyncio
import csv
from datetime import datetime
import json
import os
import sys
import time
import aiocoap

async def run_monitor(host: str, port: int, device_id: str, interval: float, log_csv: bool):
    uri = f"coap://{host}:{port}/iot/lab/{device_id}/data"
    csv_file_path = f"{device_id}_data_log.csv"

    # Khoi tao file CSV neu can ghi log
    if log_csv and not os.path.exists(csv_file_path):
        with open(csv_file_path, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Timestamp", "Device", "Temperature_C", "Humidity_Pct", "Status", "RTT_ms"])

    try:
        client = await aiocoap.Context.create_client_context()
    except Exception as e:
        print(f"Loi khoi tao CoAP Client context: {e}", flush=True)
        return

    print("=" * 60, flush=True)
    print(f"Monitoring CoAP Client started")
    print(f"Target Resource URI: {uri}")
    print(f"Poll Interval: {interval}s")
    print(f"Save CSV: {'Yes (' + csv_file_path + ')' if log_csv else 'No'}")
    print("Nhan Ctrl+C de dung giam sat.")
    print("=" * 60, flush=True)

    request_count = 0
    success_count = 0
    total_rtt_ms = 0.0

    try:
        while True:
            request_count += 1
            request_time = time.time()
            now_str = datetime.now().strftime("%H:%M:%S")

            request = aiocoap.Message(code=aiocoap.GET, uri=uri)

            try:
                # Gui request GET va cho phan hoi voi timeout 3.0s
                response = await asyncio.wait_for(client.request(request).response, timeout=3.0)
                rtt_ms = (time.time() - request_time) * 1000.0
                total_rtt_ms += rtt_ms
                success_count += 1

                payload_str = response.payload.decode("utf-8", errors="replace")
                data = json.loads(payload_str)

                dev = data.get("device_id", device_id)
                temp = float(data.get("temperature", 0.0))
                hum = float(data.get("humidity", 0.0))
                server_time = data.get("timestamp", now_str)

                # Kiem tra dieu kien canh bao theo de bai
                warnings = []
                if temp > 35.0:
                    warnings.append("CANH BAO: Nhiet do cao")
                if hum < 40.0:
                    warnings.append("CANH BAO: Do am thap")

                status_summary = "; ".join(warnings) if warnings else "Trang thai: Binh thuong"

                # Hien thi dinh dang theo mau cua docx
                print(f"[{now_str}] Received sensor data (RTT: {rtt_ms:.1f}ms)", flush=True)
                print(f"Device: {dev}", flush=True)
                print(f"Temperature: {temp:.1f} C", flush=True)
                print(f"Humidity: {hum:.1f} %", flush=True)

                if warnings:
                    for w in warnings:
                        print(w, flush=True)
                else:
                    print("Trang thai: Binh thuong", flush=True)
                print("-" * 35, flush=True)

                # Ghi ra CSV neu duoc bat
                if log_csv:
                    with open(csv_file_path, mode="a", newline="", encoding="utf-8") as f:
                        writer = csv.writer(f)
                        writer.writerow([server_time, dev, temp, hum, status_summary, f"{rtt_ms:.2f}"])

            except asyncio.TimeoutError:
                print(f"[{now_str}] Canh bao: Yeu cau GET het thoi gian cho (Timeout)! Server khong phan hoi.", flush=True)
                print("-" * 35, flush=True)
            except json.JSONDecodeError:
                print(f"[{now_str}] Loi: Khong the giai ma JSON tu payload nhan duoc: {payload_str}", flush=True)
                print("-" * 35, flush=True)
            except Exception as ex:
                print(f"[{now_str}] Loi ket noi CoAP: {ex}", flush=True)
                print("-" * 35, flush=True)

            # Cho den chu ky ke tiep
            await asyncio.sleep(interval)

    except asyncio.CancelledError:
        pass
    finally:
        print("\n" + "=" * 50, flush=True)
        print("KET THUC GIAM SAT", flush=True)
        print(f"Tong so yeu cau da gui: {request_count}", flush=True)
        print(f"So yeu cau thanh cong: {success_count}", flush=True)
        if success_count > 0:
            avg_rtt = total_rtt_ms / success_count
            print(f"Thoi gian phan hoi trung binh (Avg RTT): {avg_rtt:.2f} ms", flush=True)
        await client.shutdown()
        print("Da dong CoAP Monitoring Client.", flush=True)
        print("=" * 50, flush=True)

def main():
    parser = argparse.ArgumentParser(description="Monitoring CoAP Client - Bai 2")
    parser.add_argument("--host", default="127.0.0.1", help="Dia chi CoAP Server (mac dinh: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=5683, help="Cong CoAP (mac dinh: 5683)")
    parser.add_argument("--device", default="sensor01", help="Ma cam bien can giam sat (sensor01, sensor02, sensor03)")
    parser.add_argument("--interval", type=float, default=3.0, help="Chu ky gui request giay (mac dinh: 3.0)")
    parser.add_argument("--no-csv", action="store_true", help="Khong ghi du lieu ra file CSV")
    args = parser.parse_args()

    try:
        asyncio.run(run_monitor(args.host, args.port, args.device, args.interval, not args.no_csv))
    except KeyboardInterrupt:
        print("\nDa nhan tin hieu KeyboardInterrupt. Thoat giam sat.", flush=True)

if __name__ == "__main__":
    main()
