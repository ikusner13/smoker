import asyncio
import threading
import socket
import queue
import pprint
import msgpack
import websockets
import json

# Initialize queue and pretty printer
q = queue.Queue(64)
pp = pprint.PrettyPrinter(indent=4)

client_connected = False


# UDP Receiver Thread
class Receiver(threading.Thread):
    def __init__(self):
        self.result = None
        threading.Thread.__init__(self)

    def run(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.bind((socket.gethostname(), 65488))
            print("Receiver thread started. Listening for UDP packets...")
            while True:
                res = self.sock.recv(2048)
                if not res:
                    print("Received empty packet. Continuing...")
                    continue
                humans = msgpack.unpackb(res)
                print(f"Received UDP packet: {humans}")

                if client_connected:
                  q.put(humans, True)
        except Exception as e:
            print(f"Exception in Receiver thread: {e}")

# WebSocket Handler
async def websocket_handler(websocket, path):
  global client_connected  # Use the global flag
  client_connected = True  # Set to True when a client connects
  try:
    while True:
      if not q.empty():
        humans = q.get(True)
        print(f"Sending via WebSocket: {humans}")
        json_data = json.dumps(humans)
        await websocket.send(json_data)
        
  except websockets.exceptions.ConnectionClosedError:
      print("WebSocket connection closed.")
  except Exception as e:
      print(f"Exception occurred: {e}")

# WebSocket server in a separate thread
def websocket_server():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    start_server = websockets.serve(websocket_handler, "localhost", 8001)
    loop.run_until_complete(start_server)
    loop.run_forever()

# Main function
def main():
    # Start UDP Receiver thread
    prod_thread = threading.Thread(target=Receiver().start)
    prod_thread.start()

    # Start WebSocket server thread
    ws_thread = threading.Thread(target=websocket_server)
    ws_thread.start()

    # Wait for both threads to complete
    prod_thread.join()
    ws_thread.join()

if __name__ == '__main__':
    main()
