import argparse
import asyncio
import sys
import aiocoap

STUDENT_NAME = "Tran Han Nam"
STUDENT_ID = "B23DCCN590"

async def run_client(host: str, port: int, interactive: bool = False):
    uri = f"coap://{host}:{port}/iot/lab/message"

    try:
        client = await aiocoap.Context.create_client_context()
    except Exception as e:
        print(f"Loi khoi tao CoAP Client context: {e}")
        return

    try:
        # 1. YEU CAU GET
        print("\n" + "=" * 50)
        print("Sending GET request...")
        print(f"URI: {uri}")

        get_request = aiocoap.Message(code=aiocoap.GET, uri=uri)
        try:
            get_response = await asyncio.wait_for(client.request(get_request).response, timeout=5.0)
            print("Response:")
            print(f"  Code: {get_response.code}")
            print(f"  Payload: {get_response.payload.decode('utf-8', errors='replace')}")
        except asyncio.TimeoutError:
            print("Loi: Yeu cau GET het thoi gian cho (Timeout)! Kiem tra CoAP Server da bat chua.")
            return
        except Exception as e:
            print(f"Loi khi gui GET: {e}")
            return

        # 2. YEU CAU POST
        print("\n" + "=" * 50)
        post_content = f"Xin chao tu CoAP Client - {STUDENT_ID} - {STUDENT_NAME}"
        print("Sending POST request...")
        print(f"Payload: {post_content}")

        post_request = aiocoap.Message(
            code=aiocoap.POST,
            uri=uri,
            payload=post_content.encode("utf-8")
        )

        try:
            post_response = await asyncio.wait_for(client.request(post_request).response, timeout=5.0)
            print("Response:")
            print(f"  Code: {post_response.code}")
            print(f"  Payload: {post_response.payload.decode('utf-8', errors='replace')}")
        except asyncio.TimeoutError:
            print("Loi: Yeu cau POST het thoi gian cho (Timeout)!")
            return
        except Exception as e:
            print(f"Loi khi gui POST: {e}")
            return

        # 3. YEU CAU GET KIEM CHUNG (Mo rong: Server tra ve thong diep POST gan nhat)
        print("\n" + "=" * 50)
        print("Sending verification GET request...")
        verify_req = aiocoap.Message(code=aiocoap.GET, uri=uri)
        try:
            verify_resp = await asyncio.wait_for(client.request(verify_req).response, timeout=5.0)
            print("Response:")
            print(f"  Code: {verify_resp.code}")
            print(f"  Payload: {verify_resp.payload.decode('utf-8', errors='replace')}")
        except Exception as e:
            print(f"Loi khi kiem chung GET: {e}")

        # 4. CHE DO TUONG TAC (Mo rong: Cho phep gui tiep cac message POST tu ban phim)
        if interactive:
            print("\n" + "=" * 50)
            print("Che do Interactive POST (Nhap thong diep de gui, nhap 'EXIT' hoac Ctrl+C de dung):")
            while True:
                user_msg = await asyncio.to_thread(input, "\nNhap noi dung POST: ")
                if not user_msg or user_msg.strip().upper() == "EXIT":
                    break
                
                custom_payload = f"{user_msg.strip()} - {STUDENT_ID} - {STUDENT_NAME}"
                req = aiocoap.Message(code=aiocoap.POST, uri=uri, payload=custom_payload.encode("utf-8"))
                try:
                    res = await asyncio.wait_for(client.request(req).response, timeout=5.0)
                    print(f"Response [{res.code}]: {res.payload.decode('utf-8', errors='replace')}")
                except Exception as ex:
                    print(f"Loi khi gui POST: {ex}")

    finally:
        await client.shutdown()
        print("\nDa dong CoAP Client.")

def main():
    parser = argparse.ArgumentParser(description="CoAP Client - Bai 1")
    parser.add_argument("--host", default="127.0.0.1", help="Dia chi CoAP Server (mac dinh: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=5683, help="Cong CoAP (mac dinh: 5683)")
    parser.add_argument("--interactive", action="store_true", help="Bat che do nhap va gui POST lien tiep")
    args = parser.parse_args()

    try:
        asyncio.run(run_client(args.host, args.port, args.interactive))
    except KeyboardInterrupt:
        print("\nNhan tin hieu KeyboardInterrupt. Dung Client.")

if __name__ == "__main__":
    main()
