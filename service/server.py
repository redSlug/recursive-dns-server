"""Basic UDP server that binds to HOST and listens for
incoming datagrams
"""

import socket

from service.constants import BUFFER_SIZE, HOST, PORT


def run():
    """
    Creates a datagram socker, binds to HOST, listens for datagrams and
    sends response
    :return:
    """
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        print(f"server binding to {HOST}:{PORT}")
        s.bind((HOST, PORT))

        while True:
            message, address = s.recvfrom(BUFFER_SIZE)
            print(f"Received {message} from {address}")

            # Sending a reply to client
            bytes_to_sent = str.encode("yo, I got your message")
            s.sendto(bytes_to_sent, address)


if __name__ == "__main__":
    run()
