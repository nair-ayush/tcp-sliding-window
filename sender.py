import random
import socket
import time

# RECEIVER_IP = '10.250.96.7'
RECEIVER_IP = '10.0.0.211'
# RECEIVER_IP = socket.gethostbyname(socket.gethostname())
RECEIVER_PORT = 1024
# TEST_MESSAGES = list(range(1, 10000000))
TEST_MESSAGES = [314, 23, 44, 24.5, 5245, 2, 3, 423, 4234, 242, 34232]


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


# Function to simulate packet loss
def simulate_packet_loss():
    if random.randint(0, 9) < 3:
        return True
    return False

# Function to simulate packet corruption


def simulate_packet_corruption():
    if random.randint(0, 9) < 2:
        return True
    return False


window_size = 3

# Function to send data using the selective repeat protocol


def send_data(conn, data):
    base = 0  # Sequence number of the oldest unacknowledged packet
    next_seq_num = 0  # Sequence number of the next packet to be sent
    window = []  # Sliding window to hold the unacknowledged packets

    while base < len(data):
        # Send packets up to the window size
        while next_seq_num < base + window_size and next_seq_num < len(data):
            packet = str(next_seq_num) + ":" + str(data[next_seq_num]) + "\\"
            conn.send(packet.encode())
            window.append(next_seq_num)
            next_seq_num += 1
        # Receive acknowledgments
        while True:
            try:
                ack, _ = conn.recvfrom(1024)
                ack = int(ack.decode())
                print("ACK: ", ack)
                if ack in window:
                    window.remove(ack)
                    base = ack + 1
                if len(window) == 0:
                    break
            except socket.timeout:
                break

        # Simulate packet loss
        if simulate_packet_loss():
            print("Packet loss: ", base)
            continue

        # Simulate packet corruption
        if simulate_packet_corruption():
            print("Packet corruption: ", base)
            continue

        time.sleep(0.5)  # Simulate network delay

        # Retransmit lost or corrupted packets
        for packet_seq_num in window:
            packet = str(packet_seq_num) + ":" + data[packet_seq_num]
            conn.send(packet.encode())

    # Send the end-of-transmission packet
    conn.send("EOT".encode())


if __name__ == "__main__":
    is_success, socket_conn = start_server()
    if is_success:
        send_data(socket_conn, data=TEST_MESSAGES)
        # socket_conn.send('T'.encode('utf-8'))
        socket_conn.close()
    # socket_conn.close()
