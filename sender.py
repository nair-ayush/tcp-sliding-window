import random
import socket
import time
import lib.commonLib as lib

# RECEIVER_IP = '10.250.96.7'
RECEIVER_IP = '10.0.0.211'
RECEIVER_PORT = 1024
WINDOW_SIZE = 3
# TEST_MESSAGES = list(range(1, 10000000))
TEST_MESSAGES = [314, 23, 44, 24.5, 5245, 2, 3, 423, 4234, 242, 34232]

# Function to send data using the selective repeat protocol


def send_data(conn, data):
    """
    SELECTIVE REPEAT -- SEQUENCE NUMBER IS TWICE AS BIG AS WINDOW SIZE
    WINDOW_SIZE = 3
    SEQ_NUM = 6
    """
    base = 0  # Sequence number of the oldest unacknowledged packet
    next_seq_num = 0  # Sequence number of the next packet to be sent
    # Sliding window to hold the unacknowledged packets
    window = [-1] * WINDOW_SIZE
    max_seq_num = 2 * WINDOW_SIZE

    while base < len(data):
        # Send packets up to the window size
        while next_seq_num < base + WINDOW_SIZE and next_seq_num < len(data):
            curr_seq_num = (base + next_seq_num) % max_seq_num
            window[next_seq_num] = curr_seq_num
            packet = f"{curr_seq_num}\\"
            conn.send(packet.encode())
            next_seq_num += 1

        # Receive acknowledgments
        start_time = time.time()
        while sum(window) != -1 * WINDOW_SIZE:
            ack_message, _ = conn.recvfrom(1024)
            acks = lib.getStrippedPacket(ack_message.decode())
            for ack in acks:
                if len(ack):
                    print(f"ACK: {ack}")
                    if window[int(ack)] != -1:
                        window[int(ack)] = -1
                    else:
                        pass  # simulating acknowlegdement ignore
            if time.time() - start_time >= 5:  # wait 5 seconds and if all acks not received, then break
                break

        # Simulate packet loss
        # if lib.simulate_packet_loss():
        #     print("Packet loss: ", base)
        #     continue

        # time.sleep(0.5)  # Simulate network delay # REDUCE LATER TO 0.1

        # Retransmit lost or corrupted packets
        # for packet_seq_num in window:
        #     packet = str(packet_seq_num) + ":" + data[packet_seq_num]
        #     conn.send(packet.encode())

    # Send the end-of-transmission packet
    conn.send("EOT".encode())


if __name__ == "__main__":
    is_success, socket_conn = lib.sender_start_server(
        RECEIVER_IP, RECEIVER_PORT, WINDOW_SIZE)
    if is_success:
        send_data(socket_conn, data=TEST_MESSAGES)
        # socket_conn.send('T'.encode('utf-8'))
        socket_conn.close()
    # socket_conn.close()
