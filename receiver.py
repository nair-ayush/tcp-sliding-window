import lib.commonLib as lib

def receive_data(socket_conn, initialWindowSize):
    window = [-1]*initialWindowSize

    while True:
        packet = socket_conn.recv(1024)
        packet = packet.decode()

        # print("receiving packet --> ", packet)
        if packet == "EOT":
            print("receiving packet --> ", packet)
            break


        message = lib.getStrippedPacket(packet)
        
        for num in message: 
            if len(num):

                # Simulate packet loss
                if lib.simulate_packet_loss():
                    print("Packet loss: ", num)
                    continue
                
                if int(num) >= len(window):
                    window.extend([-1]*len(window))
                window[int(num)] = int(num) # mark packet seq number as recieved to avoid unnecessary retransmission


        # print('window = ', window)
        # Send acknowledgment
        for index,ack in enumerate(window):
            if ack!= -1:
                # print('sending ack for -->',ack)
                window[index] = -1 # mark packet as ACK sent
                socket_conn.send(f'{ack}\\'.encode())

if __name__ == "__main__":
    RECEIVER_IP = '10.0.0.211'
    RECEIVER_PORT = 1024
    connection_established, socket_conn, initialWindowSize = lib.receiver_start_server(RECEIVER_IP, RECEIVER_PORT)
    if connection_established:
        receive_data(socket_conn, initialWindowSize)
    
