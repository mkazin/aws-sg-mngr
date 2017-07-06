
class RegisteredCidr(object):
    """ Describes a registered CIDR, which provides the needed information
        to resolve the CIDR in an AWS Security Group
    """

    DO_NOT_EXPIRE = 0

    def __init__(
            self, cidr, description,
            owner=None, location=None, expiration=DO_NOT_EXPIRE):
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

        # print 'comparing {0} ({1}) to {2} ({3}):: {4}'.format(self.cidr,
        # len(self.cidr), other_cidr, len(other_cidr), result)
        return result

    def __str__(self):
        return '{{Description: "{0}", CIDR: "{1}", Owner: "{2}", Expiration: "{3}"}}' \
            .format(self.description, self.cidr, self.owner, self.expiration)
