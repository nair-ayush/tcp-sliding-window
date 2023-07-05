import socket

RECEIVER_IP = socket.gethostname()
RECEIVER_PORT = 1024


def start_server():
    # Create a TCP socket
    receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the server IP and port
    receiver_socket.bind((RECEIVER_IP, RECEIVER_PORT))

    receiver_socket.listen(10)
    print("Receiver listening on {}:{}".format(RECEIVER_IP, RECEIVER_PORT))

    # Accept a connection from a client
    client_socket, client_address = receiver_socket.accept()
    print("Accepted connection from {}:{}".format(
        client_address[0], client_address[1]))

    # Receive data from the client
    data = client_socket.recv(1024).decode('utf-8')
    print("Received data from sender:", data)

    # Send a response back to the client
    response = "Hello, sender! Successfully received message"
    client_socket.sendall(response.encode('utf-8'))

    if data == "Hello, from Project Sender!":
        return True, receiver_socket
    return False, None


if __name__ == "__main__":
    accept_messages = True
    received_messages = {}
    is_success, socket_conn = start_server()
    while accept_messages:
        data = socket_conn.recv(1024).decode('utf-8')
        if data and data.startswith('TERMINATE'):
            accept_messages = False
        elif data:
            churn = data.split(':')
            seq_num, message = churn[0], churn[1]
            received_messages[seq_num] = message
    print(received_messages)
    socket_conn.close()
