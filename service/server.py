"""Basic UDP server that binds to HOST and listens for
incoming datagrams
"""

import socket

from service.constants import BUFFER_SIZE, HOST, PORT


def get_domain_name(message):
    url_parts = list()
    start_byte = 12
    while True:
        length = message[start_byte]
        if not length:
            break

        url_part = message[start_byte + 1:start_byte + 1 + length]
        url_parts.append(url_part)
        start_byte = start_byte + length + 1

    print('.'.join([p.decode() for p in url_parts]))
    return url_parts


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
            get_domain_name(message)
            # Sending a reply to client
            bytes_to_sent = str.encode("yo, I got your message")
            s.sendto(bytes_to_sent, address)


if __name__ == "__main__":
    run()
