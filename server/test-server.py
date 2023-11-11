import socket
import time

def udp_server():
    # Create a UDP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Bind the socket to a specific address and port
    server_socket.bind((socket.gethostname(), 65487))
    
    print(f"UDP server started at {socket.gethostname()} on port 65487")

    # Initial values for setpoint and currentTemp
    setpoint = 25.0  # Example setpoint value
    currentTemp = 22.5  # Example current temperature value

    while True:
        # Format the data as a string in the required format
        data = f"setpoint={setpoint}; currentTemp={currentTemp}"
        
        # Send the data string to the specified address and port
        server_socket.sendto(data.encode(), (socket.gethostname(), 65488))
        
        print(f"Packet sent: {data}")
        
        # Increment the setpoint and currentTemp for demonstration
        setpoint += 0.1
        currentTemp += 0.1
        
        # Wait for 1 second before sending the next packet
        time.sleep(1)

# Run the UDP server
udp_server()
