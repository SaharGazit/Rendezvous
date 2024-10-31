import socket
from datetime import datetime

HOST = '0.0.0.0'
PORT = 50000

def log(message):
    print(f"[{datetime.now()}] {message}")

def handle_peer_connection(UDPServerSocket, peers):
    if len(peers) == 2:
        # Retrieve both peers from the list
        addr1, port1 = peers.pop()
        addr2, port2 = peers.pop()
        
        try:
            # Notify each peer of the other’s address and ports
            UDPServerSocket.sendto(f"{addr2};{port2 + 5};{PORT + 5}".encode('utf-8'), (addr1, port1))
            UDPServerSocket.sendto(f"{addr1};{PORT + 5};{port2 + 5}".encode('utf-8'), (addr2, port2))
            log("Connected two clients, shutting down server")
        except socket.error as e:
            log(f"Failed to send data to clients: {e}")
        return True 
    return False  

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as UDPServerSocket:
    peers = set()
    UDPServerSocket.bind((HOST, PORT))
    log("Server is activated")

    while True:
        try:
            data, (addr, port) = UDPServerSocket.recvfrom(1024)
            peer = (addr, port)

            if peer not in peers:
                peers.add(peer)
                log(f"Connection from {addr}:{port}")

            if handle_peer_connection(UDPServerSocket, peers):
                break

        except socket.error as e:
            log(f"Socket error: {e}")
