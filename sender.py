"""
AYUSH NAIR
NITISH RANJAN
"""
import socket
import time
import os
import csv

# RECEIVER_IP = '10.250.96.7'
RECEIVER_IP = '10.0.0.211'
RECEIVER_PORT = 1024
SOCKET_TIMEOUT_IN_SECONDS = 1
MAX_WINDOW_SIZE = 2**16
WINDOW_SIZE = 1
TEST_MESSAGES = list(range(1, 10**7 + 1))
WINDOW_SIZE_TRACK = []

# Function to send data using the selective repeat protocol


def sender_start_server(RECEIVER_IP, RECEIVER_PORT, WINDOW_SIZE):
    # Creates a socket object using the socket module
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Attempts to connect to the server
    conn.connect((RECEIVER_IP, RECEIVER_PORT))

    # Send data to the server
    message = f"Hello, from Project Sender! Initial window size is {WINDOW_SIZE}"
    conn.send(message.encode('utf-8'))

    # Receive a response from the server
    data = conn.recv(1024).decode('utf-8')
    print("Received data from receiver:", data)

    if data == "Hello, sender! Successfully received message":
        return True, conn
    return False, None


def getStrippedPacket(packet):
    return packet.strip().split('\\')


def send_data(conn, window_size, data):
    base = 0  # Sequence number of the latest unacknowledged packet
    next_seq_num = 0  # window packet tracker
    initial_window_expansion = True
    WINDOW_SIZE_TRACK.append((window_size, time.time()))
    while base < len(data):
        print("\n")
        print("Current window size", window_size)
        print("Progress ", f"{base} / {len(data)}",
              " -- ", "{:.2f} %".format(base / len(data) * 100))
        # window initialized to -1 and set to seq_num when corresponding packet sent
        window = [-1] * window_size
        curr_seq_num = 0
        next_seq_num = base

        # Send packets up to the window size and check for overflow beyond data length
        # next_seq_num tracks index in data items as window slides over
        # curr_seq_num tracks window seq_num
        # packets sent are marked in window an non-negative value (seq num in this case) to denote that it has been sent
        while next_seq_num < base + window_size and next_seq_num < len(data):
            window[curr_seq_num] = curr_seq_num
            packet = f"{curr_seq_num}\\"
            conn.send(packet.encode())
            curr_seq_num += 1
            next_seq_num += 1
        # print("window after send -> ", window)

        # Receive acknowledgments
        # reset packets which have been ACK'ed to -1 in window
        while sum(window) != -1 * window_size:
            try:
                ack_message, _ = conn.recvfrom(1024)
            except socket.timeout:
                break
            acks = getStrippedPacket(ack_message.decode())
            for ack in acks:
                if len(ack):
                    # print(f"ACK: {ack}")
                    if int(ack) < len(window) and window[int(ack)] != -1:
                        window[int(ack)] = -1
                    else:
                        pass  # simulating acknowlegdement ignore

        if sum(window) == -1 * window_size:  # all packets ack'ed in window
            # print('iteration success')
            base += window_size
            if initial_window_expansion:
                window_size = min(window_size*2, MAX_WINDOW_SIZE)
                print('AIMD: initial exponent increase')
            else:
                print('AIMD: additive increase')
                # additive increase
                window_size = min(window_size + 1, MAX_WINDOW_SIZE)
        else:
            # something was not ack'ed and requires retransmission
            # i.e., there is atleast one value in window [] that is non-negative
            print('AIMD: window halved')
            fail_idx = 0
            for idx in range(len(window)-1, -1, -1):
                if window[idx] > -1:
                    # print("oldest unacknowledged packet ", idx)
                    fail_idx = idx
                    break

            # set base to oldest unacknowledged packet for retransmission in next iteration
            # set window size to half
            # stop exponential window size expansion
            window_size = window_size // 2 if window_size > 1 else 1
            base = base + fail_idx
            initial_window_expansion = False
        WINDOW_SIZE_TRACK.append((window_size, time.time()))

    # Send the end-of-transmission packet
    conn.send("EOT".encode())
    print("\nEOT -- 100%")


if __name__ == "__main__":
    is_success, socket_conn = sender_start_server(
        RECEIVER_IP, RECEIVER_PORT, WINDOW_SIZE)
    if is_success:
        # reducing default timeout value
        socket_conn.settimeout(SOCKET_TIMEOUT_IN_SECONDS)
        send_data(socket_conn, WINDOW_SIZE, data=TEST_MESSAGES)
        socket_conn.close()
        start_time = WINDOW_SIZE_TRACK[0][1]
        print("Writing churn to file")
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "analysis", "window_size.csv"), "w") as wf:
            writer = csv.writer(wf)
            writer.writerow(["WINDOW_SIZE", "TIMESTAMP"])
            for window in WINDOW_SIZE_TRACK:
                a = list(window)
                a[1] = a[1] - start_time
                writer.writerow(a)
        print(f"Total Execution Time = {time.time() - start_time} seconds")
        print("__________________")
