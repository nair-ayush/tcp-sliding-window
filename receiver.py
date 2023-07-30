"""
AYUSH NAIR
NITISH RANJAN
"""
import time
import os
import csv
import socket
import random

GOOD_PUT_MOD = 1000 #calculate goodput every 1000 segments
PACKET_LOSS_PROBABILITY = 0.00001 #0.001% chance of losing a packet during transmission
seqNumbersReceived = []
seqNumbersDropped = []

def receiver_start_server(RECEIVER_IP, RECEIVER_PORT):
    # Create a TCP socket
    receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the server IP and port
    receiver_socket.bind((RECEIVER_IP, RECEIVER_PORT))

    receiver_socket.listen(1000)
    print("Receiver IP Address {}:{}".format(RECEIVER_IP, RECEIVER_PORT))

    # Accept a connection from a client
    client_socket, client_address = receiver_socket.accept()
    print("Sender IP Address {}:{}".format(
        client_address[0], client_address[1]))

    # Receive data from the client
    data = client_socket.recv(1024).decode('utf-8')
    print("Received data from sender:", data)
    WINDOW_SIZE = int(data[-1])
    print('initial window size sent from sender = ', WINDOW_SIZE)

    # Send a response back to the client -- handshake from receiver
    response = "Hello, sender! Successfully received message"
    client_socket.send(response.encode('utf-8'))

    if data.startswith("Hello, from Project Sender!"):
        return True, client_socket, WINDOW_SIZE
    return False, None, WINDOW_SIZE

# Function to simulate packet loss
def simulate_packet_loss():
    if random.random() < PACKET_LOSS_PROBABILITY:
        return True
    return False

def receive_data(socket_conn, initialWindowSize):
    
    window = [-1]*initialWindowSize
    receivedMessagesCounter = 0
    sentMessagesCounter = 0
    totalMessagesReceivedCounter = 0
    totalMessagesSentCounter = 0
    goodPutList = []

    while True:
        packet = socket_conn.recv(1024)
        packet = packet.decode()

        if packet == "EOT":
            print("Received End of Transmission Message ")
            print('Total messages sent = ',totalMessagesSentCounter)
            print('Total messages received = ',totalMessagesReceivedCounter)
            print('Average Goodput = ', '{:.2f}%'.format(sum(goodPutList)/len(goodPutList)))
            return goodPutList



        message = packet.strip().split('\\')
        
        for num in message: 
            if len(num)>0:
                if receivedMessagesCounter == GOOD_PUT_MOD:
                    goodPut = round((receivedMessagesCounter/sentMessagesCounter)*100, 4)
                    goodPutList.append(goodPut)
                    receivedMessagesCounter = 0
                    sentMessagesCounter = 0
                sentMessagesCounter += 1
                totalMessagesSentCounter += 1

                # Simulate packet loss
                if simulate_packet_loss():
                    seqNumbersDropped.append((num, time.time()))
                    continue

                #operations on packet received successfully start

                seqNumbersReceived.append((num, time.time()))
                receivedMessagesCounter += 1
                totalMessagesReceivedCounter += 1
                
                if int(num) >= len(window):
                    window.extend([-1]*len(window))
                window[int(num)] = int(num) # mark packet seq number as recieved to avoid unnecessary retransmission

                # operations on packet received successfully end

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
    connection_established, socket_conn, initialWindowSize = receiver_start_server(RECEIVER_IP, RECEIVER_PORT)
    if connection_established:
        goodPutList = receive_data(socket_conn, initialWindowSize)
    
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "analysis", "sequence number received.csv"), "w") as wf:
        writer = csv.writer(wf)
        writer.writerow(["SEQUENCE_NUMBER", "TIMESTAMP"])
        if len(seqNumbersReceived):
            start_time = seqNumbersReceived[0][1]
            for window in seqNumbersReceived:
                a = list(window)
                a[1] = a[1] - start_time
                writer.writerow(a)
    
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "analysis", "goodput over 1000.csv"), "w") as wf:
        writer = csv.writer(wf)
        writer.writerow(["steps", "Goodput"])
        if len(goodPutList):
            for i, value in enumerate(goodPutList):
                writer.writerow([i+1, value])

    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "analysis", "sequence number dropped.csv"), "w") as wf:
        writer = csv.writer(wf)
        writer.writerow(["SEQUENCE_NUMBER", "TIMESTAMP"])
        if len(seqNumbersDropped):
            start_time = seqNumbersDropped[0][1]
            for window in seqNumbersDropped:
                a = list(window)
                a[1] = a[1] - start_time
                writer.writerow(a)

            