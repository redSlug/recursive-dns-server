"""Client sending datagrams
"""

import socket

from service.constants import HOST, PORT


def send_message():
    """
    Creates a UDP socket and sends a message to the server
    :return:
    """
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect((HOST, PORT))
        print("Sending bytes to server")
        s.sendall(b"Hello, world")
        data = s.recv(1024)
    print(f"Received response {repr(data)}")


if __name__ == "__main__":
    send_message()
