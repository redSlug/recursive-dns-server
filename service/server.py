"""Basic UDP server that binds to HOST and listens for
incoming datagrams
"""

import socket

from service.request import DNSMessage

from service.constants import BUFFER_SIZE, HOST, PORT


def dig_authority_server(message, human_message):
    # b's4\x01 \x00\x01\x00\x00\x00\x00\x00\x01\x06github\x02yo\x03com\x00\x00\x01\x00\x01\x00\x00)\x10\x00\x00\x00\x00\x00\x00\x00'

    print(f"human message {human_message}")

    authority_host = "8.8.8.8"
    dns_port = 53

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect((authority_host, dns_port))
        print("Sending bytes to authority server")
        s.sendall(message)
        data = s.recv(1024)
    print(f"Received response {repr(data)}")


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
            parsed_message = DNSMessage(message, address)
            print(parsed_message.host)
            dig_authority_server(message, human_message)

            # Sending a reply to client
            bytes_to_sent = str.encode("yo, I got your message")
            s.sendto(bytes_to_sent, address)


if __name__ == "__main__":
    run()
DNSMessage
