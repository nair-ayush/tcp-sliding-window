import socket

# RECEIVER_IP = '10.250.96.7'
RECEIVER_IP = socket.gethostbyname(socket.gethostname())
RECEIVER_PORT = 1024
TEST_MESSAGES = [1, 2, 3, 4, 5, 6, -1]


def start_server():
    # Creates a socket object using the socket module
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Attempts to connect to the server
    conn.connect((RECEIVER_IP, RECEIVER_PORT))

    # Send data to the server
    message = "Hello, from Project Sender!"
    conn.sendall(message.encode('utf-8'))

    # Receive a response from the server
    data = conn.recv(1024).decode('utf-8')
    print("Received data from receiver:", data)

    if data == "Hello, sender! Successfully received message":
        return True, conn
    return False, None


def send_packets(conn):
    for packet in TEST_MESSAGES:
        conn.sendall(packet.encode('utf-8'))


if __name__ == "__main__":
    is_success, socket_conn = start_server()
    if is_success:
        send_packets(socket_conn)
        socket_conn.close()
