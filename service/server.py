"""Basic UDP server that binds to HOST and listens for
incoming datagrams
"""

import socket

from service.request import DNSMessage

from service.constants import BUFFER_SIZE, HOST, PORT


def dig_authority_server(message):
    authority_host = "8.8.8.8"
    dns_port = 53

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect((authority_host, dns_port))
        print("Sending bytes to authority server")
        s.sendall(message)
        message = s.recv(BUFFER_SIZE)
        DNSMessage(message)
    print(f"Received response {repr(message)}")


def run():
    """
    Creates a datagram socket, binds to HOST, listens for datagrams and
    sends response
    :return:
    """
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        print(f"server binding to {HOST}:{PORT}")
        s.bind((HOST, PORT))

        while True:
            message, address = s.recvfrom(BUFFER_SIZE)
            print(f"Received {message} from {address}")
            parsed_message = DNSMessage(message)
            print(parsed_message.host)
            dig_authority_server(message)

            # Sending a reply to client
            bytes_to_sent = str.encode("yo, I got your message")
            s.sendto(bytes_to_sent, address)


if __name__ == "__main__":
    run()
DNSMessage
