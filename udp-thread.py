import threading, socket, queue , pprint, msgpack

q = queue.Queue(64)
pp = pprint.PrettyPrinter(indent=4)

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
                q.put(humans, True)
        except Exception as e:
            print(f"Exception in Receiver thread: {e}")
def main():
  def producer():
    thread = Receiver()
    thread.start()
 
  def consumer():
    while True:
      humans = q.get(True)
      pp.pprint(humans)
 
  prod_thread = threading.Thread(target=producer)
  cons_thread = threading.Thread(target=consumer)
  prod_thread.start()
  cons_thread.start()
  prod_thread.join()
  cons_thread.join()

if __name__ == '__main__':
  main()