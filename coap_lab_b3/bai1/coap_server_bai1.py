import argparse
import asyncio
from datetime import datetime
import aiocoap
import aiocoap.resource as resource

class MessageResource(resource.Resource):
    """
    Tai nguyen CoAP xu ly thong diep tai /iot/lab/message.
    Ho tro:
    - GET: Tra ve thong diep chao mung tu Server.
    - POST: Nhan thong diep tu Client (ten, ma sinh vien, noi dung).
    """
    def __init__(self):
        super().__init__()
        self.latest_post_message = None

    async def render_get(self, request):
        now = datetime.now().strftime("%H:%M:%S")
        print(f"[{now}] GET request received: /iot/lab/message", flush=True)

        if self.latest_post_message:
            payload_str = f"Xin chao tu CoAP Server (Last POST: {self.latest_post_message})"
        else:
            payload_str = "Xin chao tu CoAP Server"

        return aiocoap.Message(
            code=aiocoap.CONTENT,
            payload=payload_str.encode("utf-8")
        )

    async def render_post(self, request):
        payload_str = request.payload.decode("utf-8", errors="replace")
        now = datetime.now().strftime("%H:%M:%S")

        print(f"[{now}] POST request received:", flush=True)
        print(f"  Payload: {payload_str}", flush=True)
        print(f"  Time: {now}", flush=True)

        self.latest_post_message = payload_str

        response_payload = "Server da nhan thong diep".encode("utf-8")
        return aiocoap.Message(
            code=aiocoap.CHANGED,
            payload=response_payload
        )

async def start_server(host: str, port: int):
    root = resource.Site()
    root.add_resource(["iot", "lab", "message"], MessageResource())

    server = await aiocoap.Context.create_server_context(root, bind=(host, port))

    print("=" * 60, flush=True)
    print("CoAP Server started on port", port, flush=True)
    print(f"Resource URI: coap://{host}:{port}/iot/lab/message", flush=True)
    print("Methods supported: GET, POST", flush=True)
    print("Dang cho yeu cau tu Client... (Nhan Ctrl+C de dung)", flush=True)
    print("=" * 60, flush=True)

    try:
        # Giu server chay cho den khi bi huy
        await asyncio.get_running_loop().create_future()
    except asyncio.CancelledError:
        pass
    finally:
        print("\nDang dung CoAP Server...")
        await server.shutdown()
        print("CoAP Server da dong.")

def main():
    parser = argparse.ArgumentParser(description="CoAP Server - Bai 1")
    parser.add_argument("--host", default="127.0.0.1", help="Dia chi IP bind (mac dinh: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=5683, help="Cong CoAP (mac dinh: 5683)")
    args = parser.parse_args()

    try:
        asyncio.run(start_server(args.host, args.port))
    except KeyboardInterrupt:
        print("\nDa nhan tin hieu KeyboardInterrupt. Thoat chuong trinh.")

if __name__ == "__main__":
    main()
