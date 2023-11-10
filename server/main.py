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
            humans = data.decode()
            #print(f"UDP receiver received: {humans}")
            await queue.put(humans)
        except asyncio.CancelledError:
            break
        except Exception as e:
            print(f"Exception in UDP receiver: {e}")
    sock.close()
    print("UDP receiver stopped.")

async def send_to_udp_server(host, port, message):
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        udp_sock.sendto(message, (host, port))
    finally:
        udp_sock.close()

# WebSocket handler
async def websocket_handler(websocket, path, queue):
    active_tasks = []

    async def receive_from_client():
        try:
            while not shutdown_event.is_set():
                message = await websocket.recv()
                print(f"Received from client: {message}")
                # Process the message (e.g., forward to UDP server)
                await send_to_udp_server('localhost', 65487, msgpack.packb({'message': message}))
        except websockets.exceptions.ConnectionClosed:
            print("Client disconnected. Doing cleanup.")
            cancel_tasks()
        except asyncio.CancelledError:
            pass  # Task was cancelled, normal during shutdown
        except Exception as e:
            print(f"Exception in receive_from_client: {e}")

    async def send_to_client():
        try:
            while not shutdown_event.is_set():
                humans = await queue.get()
                json_data = json.dumps(humans)
                if websocket.open:
                    await websocket.send(json_data)
                queue.task_done()
        except websockets.exceptions.ConnectionClosed:
            print("Client disconnected. Doing cleanup.")
            cancel_tasks()
        except asyncio.CancelledError:
            pass  # Task was cancelled, normal during shutdown
        except Exception as e:
            print(f"Exception in send_to_client: {e}")

    def cancel_tasks():
        for task in active_tasks:
            task.cancel()

    receive_task = asyncio.create_task(receive_from_client())
    send_task = asyncio.create_task(send_to_client())
    active_tasks.extend([receive_task, send_task])

    await asyncio.gather(*active_tasks, return_exceptions=True)
    active_tasks.clear()

async def shutdown(server, tasks):
    # Set shutdown event
    shutdown_event.set()
    
    # Close the server
    server.close()
    await server.wait_closed()

    # Cancel all running tasks
    for task in tasks:
        task.cancel()

    # Wait for tasks to finish
    await asyncio.gather(*tasks, return_exceptions=True)

async def main():
    queue = asyncio.Queue()

    # Create UDP receiver task
    udp_task = asyncio.create_task(udp_receiver(host, 65488, queue))

    # Start WebSocket server
    server = await websockets.serve(
        lambda ws, path: websocket_handler(ws, path, queue),
        "localhost", 8001
    )

    tasks = [udp_task]

    # Wait for shutdown signal
    await shutdown_event.wait()

    # Run the shutdown routine
    await shutdown(server, tasks)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Shutting down...")
        shutdown_event.set()  # Trigger the shutdown event
