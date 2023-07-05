import socket

# RECEIVER_IP = '10.250.96.7'
RECEIVER_IP = '10.0.0.211'
# RECEIVER_IP = socket.gethostbyname(socket.gethostname())
RECEIVER_PORT = 1024
TEST_MESSAGES = [1, 2, 3, 4, 5]


def start_server():
    # Creates a socket object using the socket module
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Attempts to connect to the server
    conn.connect((RECEIVER_IP, RECEIVER_PORT))

    # Send data to the server
    message = "Hello, from Project Sender!"
    conn.send(message.encode('utf-8'))

    # Receive a response from the server
    data = conn.recv(1024).decode('utf-8')
    print("Received data from receiver:", data)

    if data == "Hello, sender! Successfully received message":
        return True, conn
    return False, None


def send_packets(conn):
    PACKET_INDEX = 1
    for packet in TEST_MESSAGES:
        conn.send(f"{PACKET_INDEX}:{packet}".encode('utf-8'))
        PACKET_INDEX += 1


if __name__ == "__main__":
    is_success, socket_conn = start_server()
    if is_success:
        send_packets(socket_conn)
        socket_conn.send('T'.encode('utf-8'))
        socket_conn.close()
    # socket_conn.close()
