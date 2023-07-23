import socket
import random
import lib.commonLib as lib

# RECEIVER_IP = socket.gethostname()
RECEIVER_IP = '10.0.0.211'
RECEIVER_PORT = 1024


WINDOW_SIZE = 3
MAX_SEQ_NUM = 2*WINDOW_SIZE
window = [-1]*WINDOW_SIZE


def start_server():
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

# def receive_messages(socket_conn):
#     accept_messages_flag = True
#     received_messages = {}
#     while accept_messages_flag:
#         data = socket_conn.recv(4).decode('utf-8')
#         data = data.strip()
#         print(data.strip())
#         if data and data.find('T') > -1:
#             accept_messages_flag = False
#             print('got terminate msg')
#             socket_conn.close()
#         elif data:
#             churn = data.split(':')
#             seq_num, message = churn[0], churn[1]
#             received_messages[seq_num] = message
#     print(received_messages)
#     socket_conn.close()

# Function to simulate packet loss
def simulate_packet_loss():
    if random.randint(0, 9) < 3:
        return True
    return False


def receive_data(socket_conn):
    expected_seq_num = 0

    while True:
        packet = socket_conn.recv(1024)
        packet = packet.decode()
        print("receiving test packet ", packet)
        if packet == "EOT":
            break
        test = lib.getStrippedPacket(packet)
        print('test array ', test)
        for t in test: 
            if len(t):
                window[int(t)] = int(t)

        # Simulate packet loss
        # if simulate_packet_loss():
            # print("Packet loss: ", seq_num)
            # continue

        print('window = ', window)
        # Send acknowledgment
        for ack in window:
            if ack!= -1:
                print('sending ',ack)
                socket_conn.send(str(ack+'\\').encode())

        # Handle out-of-order packets
        # if seq_num == expected_seq_num:
        #     print("Received:", data)
        #     expected_seq_num += 1



if __name__ == "__main__":
    connection_established, socket_conn = start_server()
    if connection_established:
        # receive_messages(socket_conn)
        receive_data(socket_conn)
    
