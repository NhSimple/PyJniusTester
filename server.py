import socket
import time

# Server configuration
host = "127.0.0.1"
port = 12346

# Create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind the socket to the address and port
server_socket.bind((host, port))

# Listen for incoming connections
server_socket.listen(1)
print("Server is listening on", host, "port", port)

while True:
    # Accept a client connection
    client_socket, client_address = server_socket.accept()
    print("Accepted connection from", client_address)

    try:
        while True:
            # Send an update to the client
            update = "aa"
            client_socket.send(update.encode())

            # Wait for 1 second
            time.sleep(1)
    except KeyboardInterrupt:
        # Close the client connection when Ctrl+C is pressed
        client_socket.close()
        print("Server stopped.")
        break
