""" Represents a DNS UDP packet as described in https://tools.ietf.org/html/rfc1035 section 4.1.1

the byte order is big endian - network byte order is always big-endian,
regardless of your OS's endian-ness
"""

from bitstring import BitArray

QUESTION_BEGINNING_OFFSET = 12


class Header:
    """
    The header in a DNS UDP datagram message.

    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                      ID                       |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |QR|   Opcode  |AA|TC|RD|RA|   Z    |   RCODE   |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                    QDCOUNT                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                    ANCOUNT                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                    NSCOUNT                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                    ARCOUNT                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+


    ID              A 16 bit identifier assigned by the program that
                    generates any kind of query.  This identifier is copied
                    the corresponding reply and can be used by the requester
                    to match up replies to outstanding queries.

    QR              A one bit field that specifies whether this message is a
                    query (0), or a response (1).

    OPCODE          A four bit field that specifies kind of query in this
                    message.  This value is set by the originator of a query
                    and copied into the response.  The values are:

                    0               a standard query (QUERY)

                    1               an inverse query (IQUERY)

                    2               a server status request (STATUS)

                    3-15            reserved for future use

    AA              Authoritative Answer - this bit is valid in responses,
                    and specifies that the responding name server is an
                    authority for the domain name in question section.

                    Note that the contents of the answer section may have
                    multiple owner names because of aliases.  The AA bit

    QDCOUNT         an unsigned 16 bit integer specifying the number of
                    entries in the question section.

    ANCOUNT         an unsigned 16 bit integer specifying the number of
                    resource records in the answer section.

    NSCOUNT         an unsigned 16 bit integer specifying the number of name
                    server resource records in the authority records
                    section.

    ARCOUNT         an unsigned 16 bit integer specifying the number of
            resource records in the additional records section.


    """

    def __init__(self, bits, bytes):
        self.ID = bits[0:16]
        self.QR = bool(bits[16])
        self.Opcode = bits[17:21].int
        self.AA = False
        self.TC = False
        self.RC = False
        self.RA = False
        self.Z = False
        self.RCODE = False
        self.QDCOUNT = int.from_bytes(bytes[4:6], "big")
        self.ANCOUNT = bits[32:32 + 16].int
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


class Question:
    """

    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                                               |
    /                     QNAME                     /
    /                                               /
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                     QTYPE                     |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                     QCLASS                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

    QNAME           a domain name represented as a sequence of labels, where
                    each label consists of a length octet followed by that
                    number of octets.  The domain name terminates with the
                    zero length octet for the null label of the root.  Note
                    that this field may be an odd number of octets; no
                    padding is used.

    QTYPE           a two octet code which specifies the type of the query.
                    The values for this field include all codes valid for a
                    TYPE field, together with some more general codes which
                    can match more than one type of RR.

    QCLASS          a two octet code that specifies the class of the query.
                    For example, the QCLASS field is IN for the Internet.

    """
    def __init__(self, message):
        self.QNAME = self.get_domain_name(message)
        self.QTYPE = 'TODO'
        self.QCLASS = 'TODO'
        self.qname_end_position = self.get_qname_end_position(message)

    @staticmethod
    def get_domain_name(message):
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

    @staticmethod
    def get_qname_end_position(message):
        offset_byte = QUESTION_BEGINNING_OFFSET
        while True:
            length = message[offset_byte]
            if not length:
                break
            offset_byte = offset_byte + length + 1

        if message[offset_byte] != 0:
            raise Exception("Something has gone wrong! End of question must be a null byte")

        return offset_byte


class DNSMessage:
    def __init__(self, message):
        bits = BitArray(message)

        self.message = message
        self.count = len(bits)
        self.header = Header(bits, message)

        if self.header.QDCOUNT != 1:
            raise Exception("Case w/ more than one question unimplemented")

        self.question = Question(message)
        self.host = self.question.QNAME
        self.ip_address = self.get_ip_address()

    def __repr__(self):
        return f"""{self.count} bit message ({self.header.ID}):
            {self.header}
        """

    def get_first_answer_offset(self):
        if self.header.QDCOUNT != 1:
            raise Exception("Case w/ more than one question unimplemented")

        offset_byte = QUESTION_BEGINNING_OFFSET
        while True:
            length = self.message[offset_byte]
            if not length:
                break
            offset_byte = offset_byte + length + 1

        return offset_byte

    def get_ip_address(self):
        qname_end = self.question.get_qname_end_position(self.message)
        qclass_end = qname_end + 4
        answer_beginning = qclass_end
        rd_length = int.from_bytes(self.message[answer_beginning:answer_beginning+1], "big")
        print("rd length", rd_length)
        ip_address = self.message[offset + 2 : offset + 2 + rd_length]
        print(ip_address)
        return 1
