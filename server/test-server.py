import socket
import time
import msgpack

def udp_server():
    # Create a UDP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Bind the socket to a specific address and port
    server_socket.bind((socket.gethostname(), 65487))
    
    print(f"UDP server started at {socket.gethostname()} on port 65487")

    count = 0
    while True:
        # Create a sample packet as a Python dictionary
        data = {"count": count, "message": "Hello, world!"}
        
        # Serialize the data using msgpack
        serialized_data = msgpack.packb(data)
        
        # Send the serialized data to the same address and port (for demonstration)
        server_socket.sendto(serialized_data, (socket.gethostname(), 65488))
        
        print(f"Packet sent: {data}")
        
        # Increment the count
        count += 1
        
        # Wait for 1 second before sending the next packet
        time.sleep(1)

# Run the UDP server
udp_server()
