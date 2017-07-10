from aws_sg_mngr.server import app
from aws_sg_mngr.registeredCidr import RegisteredCidr
from aws_sg_mngr.awsSecurityGroup import ALL_PROTOCOLS

import boto3
import json
# import mock
from moto import mock_ec2
import unittest
# from botocore.stub import Stubber
# from tests.mockClient import MockClient


@mock_ec2
class ServerTests(unittest.TestCase):

    # TEST_GROUP_ID = 'sg-ebe1ac8f'
    TEST_GROUP_NAME = 'TestSecurityGroup'
    TEST_GROUP_DESCRIPTION = 'A mock security group'
    TEST_GROUP_ID = None

    # def __init__(self):
    #     super.__init__()
    #     self.TEST_GROUP_ID = None

    # def setUp(self):
    @classmethod
    @mock_ec2
    def setUpClass(self):
        # super(cls).setUpClass()

        # self = cls
        self.app = app.test_client()
        self.app.testing = True
        # self.app.client = stubber  # MockClient()

        if self.TEST_GROUP_ID is None:
            client = boto3.client('ec2', 'us-east-1',
                                  aws_access_key_id='test_key',
                                  aws_secret_access_key='test_secret')
            response = client.create_security_group(
                GroupName=ServerTests.TEST_GROUP_NAME,
                Description=ServerTests.TEST_GROUP_DESCRIPTION)

            print(response)
            self.TEST_GROUP_ID = response['GroupId']

        # client.
        # stubber = Stubber(self.app.mngr.client)
        # with open('tests/example-security-group.txt', 'r') as testfile:
        #     describe_groups_response = json.load(testfile)
        # stubber.add_response('describe_security_groups', describe_groups_response)

        # cidr = RegisteredCidr(
        #     cidr=cidr_str, description=description, owner=owner,
        #     location=location, expiration=RegisteredCidr.DO_NOT_EXPIRE)

        # self.app.store.store_cidr(cidr)

# def test_init(self):
#     raise NotImplementedError()


# def test_get_groups(self):
#     # @api.route('/api/groups')
#     # def get(self):
#     raise NotImplementedError()

    # @mock.patch('aws_sg_mngr.server.api')
    def test_get_single_group(self):  # , mock_api):

        # mock_api.get_security_groups.return_value = {'Boo': 32}
        # print('Stubber: ', stubber.describe_security_groups())

        # with stubber:
        response = self.app.get('/api/groups/{0}'.format(self.TEST_GROUP_ID))
        assert response.status_code == 200
        sgs = json.loads(response.data.decode(encoding='utf-8'))

        sg = sgs[0]
        print('sg:', sg)
        assert sg['Description'] == ServerTests.TEST_GROUP_DESCRIPTION
        assert sg['GroupId'] == ServerTests.TEST_GROUP_ID
        assert sg['GroupName'] == ServerTests.TEST_GROUP_NAME

        assert len(sg['Rules']) == 1
        assert sg['Rules'][0]['IpProtocol'] == ALL_PROTOCOLS
        assert sg['Rules'][0]['Cidr'] == "0.0.0.0/0"

        # @api.route('/api/groups/<string:group_id>')
        # def get(self, group_id):


# def test_query_registered_cidrs(self):
#     # query_registered_cidrs(self):
#     raise NotImplementedError()

# # @cidrs_namespace.route('/')


# def test_post_cidr(self):
#     # @api.route('/cidr')
#     #     def post(self):
#     raise NotImplementedError()


# def test_post_rule(self):
#     # @api.route('/api/rules/<string:group_id>')
#     #     def post(self, group_id):
#     raise NotImplementedError()

    def test_root(self):
        result = self.app.get('/')
        print('Result:', result)
        assert result

        # @app.route('/')
        # def hello_world(self):
