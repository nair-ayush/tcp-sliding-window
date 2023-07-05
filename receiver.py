import socket

# RECEIVER_IP = socket.gethostname()
RECEIVER_IP = '10.0.0.211'
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
    client_socket.send(response.encode('utf-8'))

    if data == "Hello, from Project Sender!":
        return True, client_socket
    return False, None

def receive_messages(is_success, socket_conn):
    accept_messages_flag = True
    received_messages = {}
    while accept_messages_flag:
        data = socket_conn.recv(4).decode('utf-8')
        data = data.strip()
        print(data.strip())
        if data and data.startswith('T'):
            accept_messages_flag = False
            print('got terminate msg')
            socket_conn.close()
        elif data:
            churn = data.split(':')
            seq_num, message = churn[0], churn[1]
            received_messages[seq_num] = message
    print(received_messages)
    # socket_conn.close()


if __name__ == "__main__":
    is_success, socket_conn = start_server()
    receive_messages(is_success, socket_conn)
    
