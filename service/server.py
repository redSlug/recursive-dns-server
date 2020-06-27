"""Basic UDP server that binds to HOST and listens for
incoming datagrams
"""

import socket

from service.constants import BUFFER_SIZE, HOST, PORT

QUESTION_BEGINNING_OFFSET = 12


def get_domain_name(message):
    url_parts = list()
    start_byte = QUESTION_BEGINNING_OFFSET
    while True:
        length = message[start_byte]
        if not length:
            break

        url_part = message[start_byte + 1:start_byte + 1 + length]
        url_parts.append(url_part)
        start_byte = start_byte + length + 1

    return '.'.join([p.decode() for p in url_parts])


def get_first_answer_offset(message):
    # NOTE(bdettmer): for now, assuming one question, but later will need to parse the header to get
    # question count, which is qd_count = message[4:6]

    offset_byte = QUESTION_BEGINNING_OFFSET  # question beginnning
    while True:
        length = message[offset_byte]
        if not length:
            # offset byte is zero, reached delimeter
            break
        offset_byte = offset_byte + length + 1

    return offset_byte


def get_ip_address(message):
    message = b'\xf5\xfa\x81\x80\x00\x01\x00\x01\x00\x00\x00\x01\x06github\x02yo\x03com\x00\x00\x01\x00\x01\xc0\x0c\x00\x01\x00\x01\x00\x00\r\xc1\x00\x04E\xac\xc9\x99\x00\x00)\x02\x00\x00\x00\x00\x00\x00\x00'

    offset = get_first_answer_offset(message)
    length_of_domain = offset - QUESTION_BEGINNING_OFFSET

    # advance 6 bytes for type, class, TTL
    offset = offset + length_of_domain + 6
    rd_length = message[offset:offset + 2]
    rd_length = int.from_bytes(rd_length, byteorder='little')
    breakpoint()
    print("rd length", rd_length)
    ip_address = message[offset + 2: offset + 2 + rd_length]
    print(ip_address)

    # NOTE(bdettmer): for now just getting first answer, but later we can look at ANCOUNT to get
    # the amount of answers and return them all

get_ip_address(1)


def dig_authority_server(message, human_message):
    # b's4\x01 \x00\x01\x00\x00\x00\x00\x00\x01\x06github\x02yo\x03com\x00\x00\x01\x00\x01\x00\x00)\x10\x00\x00\x00\x00\x00\x00\x00'

    print(f"human message {human_message}")

    authority_host = '8.8.8.8'
    dns_port = 53

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect((authority_host, dns_port))
        print("Sending bytes to authority server")
        s.sendall(message)
        data = s.recv(1024)
    print(f"Received response {repr(data)}, {get_domain_name(data)}")


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
            human_message = get_domain_name(message)

            dig_authority_server(message, human_message)

            # Sending a reply to client
            bytes_to_sent = str.encode("yo, I got your message")
            s.sendto(bytes_to_sent, address)


if __name__ == "__main__":
    run()
