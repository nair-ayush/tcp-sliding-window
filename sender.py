import socket
import lib.commonLib as lib

# RECEIVER_IP = '10.250.96.7'
RECEIVER_IP = '10.0.0.211'
RECEIVER_PORT = 1024
MAX_WINDOW_SIZE = 10**16
WINDOW_SIZE = 4
TEST_MESSAGES = list(range(1, 100000))

# Function to send data using the selective repeat protocol


def send_data(conn, window_size, data):
    base = 0  # Sequence number of the latest unacknowledged packet
    next_seq_num = 0  # window packet tracker
    initial_window_expansion = True
    while base < len(data):
        print("\n")
        print("Current window size", window_size)
        print("Progress ", f"{base} / {len(data)}",
              " -- ", f"{base / len(data) * 100} %")
        # window initialized to -1 and set to seq_num when corresponding packet sent
        window = [-1] * window_size
        curr_seq_num = 0
        next_seq_num = base

        # Send packets up to the window size and check for overflow beyond data length
        # next_seq_num tracks index in data items as window slides over
        # curr_seq_num tracks window seq_num
        while next_seq_num < base + window_size and next_seq_num < len(data):
            window[curr_seq_num] = curr_seq_num
            packet = f"{curr_seq_num}\\"
            conn.send(packet.encode())
            curr_seq_num += 1
            next_seq_num += 1
        # print("window after send -> ", window)

        # Receive acknowledgments
        while sum(window) != -1 * window_size:
            try:
                ack_message, _ = conn.recvfrom(1024)
            except socket.timeout:
                break
            acks = lib.getStrippedPacket(ack_message.decode())
            for ack in acks:
                if len(ack):
                    # print(f"ACK: {ack}")
                    if window[int(ack)] != -1:
                        window[int(ack)] = -1
                    else:
                        pass  # simulating acknowlegdement ignore

        if sum(window) == -1 * window_size:  # all packets ack'ed in window
            # print('iteration success')
            base += window_size
            if initial_window_expansion:
                window_size *= 2
                print('AIMD: initial exponent increase')
            else:
                print('AIMD: additive increase')
                window_size = min(window_size + 1, MAX_WINDOW_SIZE)  # additive increase
        else:
            print('AIMD: window halved')
            # something was not ack'ed and requires retransmission
            fail_idx = 0
            for idx in range(len(window)-1, -1, -1):
                if window[idx] > -1:
                    # print("oldest unacknowledged packet ", idx)
                    fail_idx = idx
                    break

            window_size = window_size // 2 if window_size > 1 else 1

            base = base + fail_idx
            initial_window_expansion = False

    # Send the end-of-transmission packet
    conn.send("EOT".encode())
    print("\nEOT")


if __name__ == "__main__":
    is_success, socket_conn = lib.sender_start_server(
        RECEIVER_IP, RECEIVER_PORT, WINDOW_SIZE)
    if is_success:
        socket_conn.settimeout(1)
        send_data(socket_conn, WINDOW_SIZE, data=TEST_MESSAGES)
        socket_conn.close()
