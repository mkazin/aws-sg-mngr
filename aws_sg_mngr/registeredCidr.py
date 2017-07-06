# TODO: Consider using this built-in class instead of strings. This would simplify error handling
# it also provides us with compare functionality like "contains()" and superset() function to simplify storage
from ipaddress import IPv4Network


class RegisteredCidr(object):
    """ Describes a registered CIDR, which provides the needed information
        to resolve the CIDR in an AWS Security Group
    """

    DO_NOT_EXPIRE = 0

    def __init__(self, cidr, description, owner=None, location=None, expiration=DO_NOT_EXPIRE):
        try:
            self.cidr = cidr.decode('utf-8')
        except AttributeError:
            self.cidr = cidr

        self.description = description
        self.location = location
        self.owner = owner
        self.expiration = expiration

    def matches(self, other_cidr):
        # other_cidr = other_cidr.decode('utf-8')

        if isinstance(other_cidr, self.__class__):
            result = self.cidr == other_cidr.cidr
        else:
            result = False

        # print 'comparing {} ({}) to {} ({}):: {}'.format(self.cidr,
        # len(self.cidr), other_cidr, len(other_cidr), result)
        return result

    def __str__(self):
        return '{{Description: "{}", CIDR: "{}", Owner: "{}", Expiration: "{}"}}' \
            .format(self.description, self.cidr, self.owner, self.expiration)
