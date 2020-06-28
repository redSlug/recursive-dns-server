from service.request import DNSMessage

DUMMY_MESSAGE = b"\xf5\xfa\x81\x80\x00\x01\x00\x01\x00\x00\x00\x01\x06github\x02yo\x03com\x00\x00\x01\x00\x01\xc0\x0c\x00\x01\x00\x01\x00\x00\r\xc1\x00\x04E\xac\xc9\x99\x00\x00)\x02\x00\x00\x00\x00\x00\x00\x00"


def test_get_message_host():
    message = DNSMessage(DUMMY_MESSAGE)
    assert message.host == "github.yo.com"


def test_get_qname_end():
    message = DNSMessage(DUMMY_MESSAGE)
    assert message.question.qname_end_position


def test_get_message_ip():
    message = DNSMessage(DUMMY_MESSAGE)
    assert message.ip_address
