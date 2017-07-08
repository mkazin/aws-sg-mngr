
class CidrStore(object):

    def store_cidr(self, cidr):
        raise NotImplemented('Abstract function must be overriden')

    def query_all(self):
        raise NotImplemented('Abstract function must be overriden')

    def query_one(self, cidr_str):
        raise NotImplemented('Abstract function must be overriden')
