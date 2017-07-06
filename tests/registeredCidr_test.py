from aws_sg_mngr import registeredCidr


def test_matches():

    cidr_a = registeredCidr.RegisteredCidr(
        '8.8.8.8/32', 'Simple CIDR', 'Google', 'Mountain View')

    assert cidr_a.matches(cidr_a)
    assert not cidr_a.matches("non sequitur")

    cidr_b = registeredCidr.RegisteredCidr(
        '8.8.8.8/32', 'Same CIDR, Different Object', 'Google', 'Mountain View')

    assert cidr_a.matches(cidr_b)


    # Unicode input should match utf-8
    unicode_cidr = registeredCidr.RegisteredCidr(
        u'8.8.8.8/32', 'Google DNS as unicode', 'Google', 'Mountain View')

    string_cidr = registeredCidr.RegisteredCidr(
        '8.8.8.8/32', 'Google DNS as unicode', 'Google', 'Mountain View')

    assert unicode_cidr.matches(string_cidr)
