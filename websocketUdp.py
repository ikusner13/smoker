import asyncio
import socket
import websockets
from asyncio.queues import Queue
import json

# UDP setup
UDP_PORT = 2390
UDP_IP = "192.168.43.255"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
sock.bind((UDP_IP, UDP_PORT))

# Create a Queue
queue = asyncio.Queue()

# UDP Listener
def udp_listener(queue: Queue):
    while True:
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        print("received message: %s" % data)
        queue.put_nowait(data.decode())

# WebSocket Handler
async def handler(websocket):
    while True:
        message = await queue.get()
        print(f">>> {message}")
        await websocket.send(json.dumps(message))
        await asyncio.sleep(1)

# Main function
async def main():
    loop = asyncio.get_running_loop()

    # Start UDP Listener in the background
    loop.run_in_executor(None, udp_listener, queue)

    # Start WebSocket Server
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Shutting down due to KeyboardInterrupt...")
        sock.close()  # Don't forget to close the socket
        print("Server has shutdown")