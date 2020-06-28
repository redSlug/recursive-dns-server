from bitstring import BitArray

QUESTION_BEGINNING_OFFSET = 12


class Header:
    def __init__(self, id, qr, op_code):
        self.ID = id
        """
        A 16 bit identifier assigned by the program that generates any kind
        of query.  This identifier is copied the corresponding reply
        and can be used by the requester to match up replies
        to outstanding queries.
        """

        self.QR = qr
        """
        A one bit field that specifies whether this message is a query (0),
        or a response (1).
        """

        self.Opcode = op_code
        """
        A four bit field that specifies kind of query in this
        message.  This value is set by the originator of a query
        and copied into the response.  The values are:

        0               a standard query (QUERY)

        1               an inverse query (IQUERY)

        2               a server status request (STATUS)

        3-15            reserved for future use
        """

        self.AA = False
        self.TC = False
        self.RC = False
        self.RA = False
        self.Z = False
        self.RCODE = False
        self.QDCOUNT = []
        self.ANCOUNT = []
        self.NSCOUNT = []
        self.ARCOUNT = []

    def __repr__(self):
        return f"""
            QR: {self.QR}
            Opcode: {self.Opcode}
            AA: {self.AA}
            TC: {self.TC}
            RC: {self.RC}
            RA: {self.RA}
            Z: {self.Z}
            RCODE: {self.RCODE}
            QDCOUNT: {self.QDCOUNT}
            ANCOUNT: {self.ANCOUNT}
            NSCOUNT: {self.NSCOUNT}
        """


class DNSMessage:
    def __init__(self, message):
        # number of bytes in packet
        bits = BitArray(message)

        self.count = len(bits)
        self.header = Header(id=bits[0:16], qr=bool(bits[16]), op_code=(bits[17:21]).int)
        self.host = self.get_domain_name(message)
        self.ip_address = self.get_ip_address(message)

    def __repr__(self):
        return f"""{self.count} bit message ({self.header.ID}):
            {self.header}
        """

    def get_domain_name(self, message):
        url_parts = list()
        start_byte = QUESTION_BEGINNING_OFFSET
        while True:
            length = message[start_byte]
            if not length:
                break

            url_part = message[start_byte + 1 : start_byte + 1 + length]
            url_parts.append(url_part)
            start_byte = start_byte + length + 1

        return ".".join([p.decode() for p in url_parts])

    def get_first_answer_offset(self, message):
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

    def get_ip_address(self, message):
        offset = self.get_first_answer_offset(message)
        length_of_domain = offset - QUESTION_BEGINNING_OFFSET

        # advance 6 bytes for type, class, TTL
        offset = offset + length_of_domain + 6
        rd_length = message[offset : offset + 2]
        rd_length = int.from_bytes(rd_length, byteorder="little")
        breakpoint()
        print("rd length", rd_length)
        # NOTE(bdettmer): for now just getting first answer, but later we can look at ANCOUNT to get
        # the amount of answers and return them all
        ip_address = message[offset + 2 : offset + 2 + rd_length]
        print(ip_address)
        return 1


if __name__ == "__main__":
    dummy_message = b"\xf5\xfa\x81\x80\x00\x01\x00\x01\x00\x00\x00\x01\x06github\x02yo\x03com\x00\x00\x01\x00\x01\xc0\x0c\x00\x01\x00\x01\x00\x00\r\xc1\x00\x04E\xac\xc9\x99\x00\x00)\x02\x00\x00\x00\x00\x00\x00\x00"
    DNSMessage(dummy_message)
