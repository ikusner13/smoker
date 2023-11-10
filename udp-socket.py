import asyncio
import socket
import websockets
import msgpack
import json

host = socket.gethostname()

shutdown_event = asyncio.Event()

# Asynchronous UDP receiver
async def udp_receiver(host, port, queue):
    print("UDP receiver started")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))
    sock.setblocking(False)

    while not shutdown_event.is_set():
        try:
            data = await asyncio.get_event_loop().sock_recv(sock, 1024)
            humans = msgpack.unpackb(data)
            print(f"UDP receiver received: {humans}")
            await queue.put(humans)
        except asyncio.CancelledError:
            break
        except Exception as e:
            print(f"Exception in UDP receiver: {e}")
    sock.close()
    print("UDP receiver stopped.")

# WebSocket handler
async def websocket_handler(websocket, path, queue):
    while not shutdown_event.is_set():
        try:
            humans = await queue.get()
            json_data = json.dumps(humans)
            print(f">>> {json_data}")
            await websocket.send(json_data)
        except asyncio.CancelledError:
            break
        except Exception as e:
            print(f"Exception in WebSocket handler: {e}")

# Manual shutdown trigger
async def manual_shutdown():
    await asyncio.to_thread(input, "Press Enter to stop the server...\n")
    shutdown_event.set()

# Main coroutine
async def main():
    queue = asyncio.Queue()
    udp_task = asyncio.create_task(udp_receiver(host, 65488, queue))
    ws_server = await websockets.serve(
        lambda ws, path: websocket_handler(ws, path, queue),
        "localhost", 8001
    )

    await manual_shutdown()
    udp_task.cancel()
    ws_server.close()
    await ws_server.wait_closed()
    print("WebSocket server stopped.")

# Run the main coroutine
asyncio.run(main())
