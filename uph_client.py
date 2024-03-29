import socket
import random
import threading

rendezvous = ('127.0.0.1', 50_000)

# TODO: send Keep-Alive packets

HOST = f"127.0.0.{random.randint(1, 100)}"

# get other peer connection details (address, port) from the rendezvous server
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    sock.bind((HOST, 50500+random.randint(1, 100)))
    sock.sendto("hello".encode('utf-8'), rendezvous)

    data = []
    while True:
        data = sock.recvfrom(1024)[0].decode('utf-8').split(';')
        if len(data) == 3:
            print("data:", data)
            break

    peer_addr, peer_port, own_port = data
    peer_port = int(peer_port)
    own_port = int(own_port)

    peer = (peer_addr, peer_port)


# hole punching
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    sock.bind((HOST, own_port))
    print(f"Listening on {own_port}..\n")

    sock.sendto("punching hole".encode('utf-8'), peer)


# receive messages from peer in another thread
def recv_msgs():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((HOST, own_port))
        print("own_port:", own_port)
        while True:
            data, addr = sock.recvfrom(1024)
            print(f"Peer: {data.decode('utf-8')}\n> ")


recv_msgs_thread = threading.Thread(target=recv_msgs)
recv_msgs_thread.start()


# send udp messages
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    # when sending UDP packets, bind to the other peer port
    sock.bind((HOST, peer_port))

    while True:
        msg = input("> ")
        sock.sendto(msg.encode('utf-8'), peer)