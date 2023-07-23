import random
import socket



def receiver_start_server(RECEIVER_IP, RECEIVER_PORT):
    # Create a TCP socket
    receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the server IP and port
    receiver_socket.bind((RECEIVER_IP, RECEIVER_PORT))

    receiver_socket.listen(1000)
    print("Receiver listening on {}:{}".format(RECEIVER_IP, RECEIVER_PORT))

    # Accept a connection from a client
    client_socket, client_address = receiver_socket.accept()
    print("Accepted connection from {}:{}".format(
        client_address[0], client_address[1]))

    # Receive data from the client
    data = client_socket.recv(1024).decode('utf-8')
    print("Received data from sender:", data)
    WINDOW_SIZE = int(data[-1])
    window = [-1]*WINDOW_SIZE
    print('initial window size sent from sender = ', WINDOW_SIZE)

    # Send a response back to the client -- handshake from receiver
    response = "Hello, sender! Successfully received message"
    client_socket.send(response.encode('utf-8'))

    if data.startswith("Hello, from Project Sender!"):
        return True, client_socket
    return False, None


def getStrippedPacket(packet):
    return packet.strip().split('\\')

# Function to simulate packet loss
def simulate_packet_loss():
    if random.randint(0, 9) < 3:
        return True
    return False