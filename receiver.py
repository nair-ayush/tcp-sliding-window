import lib.commonLib as lib

RECEIVER_IP = '10.0.0.211'
RECEIVER_PORT = 1024


WINDOW_SIZE = 3
MAX_SEQ_NUM = 2*WINDOW_SIZE
window = [-1]*WINDOW_SIZE
EOT = False


def receive_data(socket_conn):

    while not EOT:
        packet = socket_conn.recv(1024)
        packet = packet.decode()

        print("receiving test packet ", packet)
        if packet == "EOT":
            break

        message = lib.getStrippedPacket(packet)
        print('message ', message)
        
        for num in message: 
            if len(num):
                window[int(num)] = int(num)

        # Simulate packet loss
        # if lib.simulate_packet_loss():
            # print("Packet loss: ", seq_num)
            # continue

        print('window = ', window)
        # Send acknowledgment
        for index,ack in enumerate(window):
            if ack!= -1:
                print('sending ',ack)
                window[index] = -1
                socket_conn.send(f'{ack}\\'.encode())
        



if __name__ == "__main__":
    connection_established, socket_conn = lib.receiver_start_server(RECEIVER_IP, RECEIVER_PORT)
    if connection_established:
        # receive_messages(socket_conn)
        receive_data(socket_conn)
    
