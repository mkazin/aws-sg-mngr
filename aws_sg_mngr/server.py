import configparser
from flask import Flask, Blueprint
from flask_restplus import Resource, Api
from flask_restful_swagger import swagger
from flask_restful import fields, marshal

from aws_sg_mngr.registeredCidr import RegisteredCidr
from aws_sg_mngr.awsSecurityGroup import AwsSecurityGroups
from aws_sg_mngr.marshaller import Marshaller
from aws_sg_mngr import api as mngr_api

# import registeredCidr
import json
import boto3
from botocore.exceptions import NoCredentialsError
# import marshaller
import logging
from logging.handlers import RotatingFileHandler
import sqlite3

# TODO: remove when I'm no longer setting environment variable for testing
import os


app = Flask(__name__)
api = Api(app)
# sgs_namespace = api.namespace(
#     'groups', description='Operations related to security groups')
# cidrs_namespace = api.namespace(
#     'cidrs', description='Operations related to registered CIDRs')


def initialize_app():
    app.logger.setLevel(logging.DEBUG)
    file_handler = RotatingFileHandler(
        'flask.log', maxBytes=1024 * 1024 * 100, backupCount=3)
    file_handler.setLevel(logging.DEBUG)
    app.logger.addHandler(file_handler)

    # Set up the flast_restplus API
    # See
    # http://michal.karzynski.pl/blog/2016/06/19/building-beautiful-restful-apis-using-flask-swagger-ui-flask-restplus/
    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)

    # api.add_namespace(sgs_namespace)
    # api.add_namespace(cidrs_namespace)

    app.register_blueprint(blueprint)


# Set up Swagger Docs
# See http://github.com/rantav/flask-restful-swagger
# NOTE: this may not be needed. See if flask_restplus already provides this
#api = swagger.docs(Api(app), apiVersion='0.1')

CONFIG_FILE = 'aws_sg_mngr/config/boto.cfg'
REGION = 'us-east-1'

config = configparser.ConfigParser()
config.read(CONFIG_FILE)
print(','.join(str(x) for x in config.keys()))
db_filename = config.get('DB', 'path')
conn = sqlite3.connect(db_filename)


# @sgs_namespace.route('/')
@api.route('/api/groups')
# Consider using flask_restful.marshal_with_fields - see:
#    http://stackoverflow.com/questions/22645029
class SecurityGroupsCollection(Resource):

    def get(self):
        print('GET groups')
        mngr = mngr_api.Api(REGION)
        aws_groups = mngr.get_security_groups()

        cidrs = get_registered_cidrs()  # TODO: replace with persistence
        data = Marshaller.merge_records(cidrs, aws_groups)

        return data

        # NOTE: disabling marshalling
        # print('******* OUTPUT ************')
        # print('data: {0}'.format(data))
        # result = Marshaller._marshall_records_(data)
        # print('Result: ', result)
        # return result


@api.route('/api/groups/<string:group_id>')
# Consider using flask_restful.marshal_with_fields - see:
#    http://stackoverflow.com/questions/22645029
class SecurityGroup(Resource):

    def get(self, group_id):

        parts = group_id.split('-')
        assert parts[0] == 'sg'

        print('GET group {0}'.format(group_id))
        mngr = mngr_api.Api(REGION)
        aws_groups = mngr.get_security_groups(group_ids=[group_id])

        cidrs = get_registered_cidrs()  # TODO: replace with persistence
        data = Marshaller.merge_records(cidrs, aws_groups)

        return data


def get_registered_cidrs():
    cidrs = []
    # TODO: test expiration:: , expiration=DO_NOT_EXPIRE))
    cidrs.append(RegisteredCidr(
        "209.6.37.244/32", "Home", owner="mjkazin", location="Home"))
    cidrs.append(RegisteredCidr(
        "75.67.236.14/32", "Company HQ", owner="mjkazin",
        location="Office"))  # TODO: test expiration:: , expiration=DO_NOT_EXPIRE))
    return cidrs


# @cidrs_namespace.route('/')
@api.route('/cidr')
class SecurityGroupRule(Resource):

    @api.response(201, 'Rule successfully created.')
    def post(self):
        """Creates a new blog category."""
        mngr = mngr_api.Api(REGION)
        mngr.create_rule(request.json)
        return None, 201


@app.route('/')
def hello_world():
    # return 'Hello, World!'

    # Merge our data into AWS' .  For more see:
    #   https://flask-restful.readthedocs.io/en/0.3.5/fields.html#complex-structures

    with open('server/example-security-group.txt', 'r') as stub_group:
        aws_groups = json.load(stub_group)

    mngr_records = [
        RegisteredCidr('209.6.205.245/32', 'Mike home', owner='mike',
                       location='Somerville, MA',
                       expiration=RegisteredCidr.DO_NOT_EXPIRE),
        RegisteredCidr('96.95.188.89/32', 'Work', owner='mike',
                       location='123 Summer St. Boston, MA',
                       expiration=RegisteredCidr.DO_NOT_EXPIRE)
    ]
#        mngr_cidr = next((x for x in mngr_sgs if x['CidrIp'] == curr['CidrIp']), None)
#        cidr_info = {}
#        if mngr_group is not None:
#            cidr_info['Owner'] = mngr_cidr['Owner']
#            cidr_info['Description'] = mngr_cidr['Description']

    merged = merge_records(mngr_records, aws_groups)
    print('Merged: {0}'.format(merged))
    marshalled = marshall_records(merged)
    return marshalled
    #json.dumps(marshalled, sort_keys=True, indent=4, separators=(',', ': '))

    # return json.dumps(groups)


@app.route('/testMerge')
def test_route():
    with open('example-security-group.txt', 'r') as stub_group:
        stub_data = json.load(stub_group)
    aws_groups = stub_data['SecurityGroups']

    merged = merge_records(mngr_sgs, aws_groups)

    assert(len(merged) == 0)
    sg = merged[0]
    assert(sg['GroupId'] == 'sg-ebe1ac8f')


@app.route('/testBoto')
def test_boto():

    os.environ['BOTO_CONFIG'] = CONFIG_FILE

    session = boto3.session.Session()
    client = session.client(service_name='ec2', region_name=REGION)

    groups = AwsSecurityGroups.from_boto(client)

    # response = client.describe_security_groups()

    print(groups)
    return str(groups)

    # if response['ResponseMetadata']['HTTPStatusCode'] != 200:
    #     print 'Error getting SecurityGroup data from AWS:',
    #     print response['ResponseMetadata']
    #     return

    # response['SecurityGroups']

    # client.authorize_security_group_egress(self, *args, **kwargs)


if __name__ == '__main__':
    initialize_app()
    app.run(debug=True)
