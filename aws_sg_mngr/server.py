import configparser
from flask import Flask, Blueprint
from flask_restplus import Resource, Api
# from flask_restful_swagger import swagger
from flask_restful import fields, marshal

from aws_sg_mngr.registeredCidr import RegisteredCidr
from aws_sg_mngr.awsSecurityGroup import AwsSecurityGroups
from aws_sg_mngr.marshaller import Marshaller
from aws_sg_mngr import api as mngr_api
from aws_sg_mngr.sqliteStore import SqliteStore

import json
import boto3
from botocore.exceptions import NoCredentialsError

import logging
from logging.handlers import RotatingFileHandler

# TODO: remove when I'm no longer setting environment variable for testing
import os


# TODO: remove this hack. See the Flaskr example which uses a factory
#       to create the application
CONFIG_FILE = 'config/boto.cfg'
if not os.path.exists(CONFIG_FILE):
    CONFIG_FILE = 'tests/test_server.cfg'

REGION = 'us-east-1'

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

    initialize_db()

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
# api = swagger.docs(Api(app), apiVersion='0.1')


def initialize_db():

    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    app.store = SqliteStore(config)


@api.route('/api/groups')
# Consider using flask_restful.marshal_with_fields - see:
#    http://stackoverflow.com/questions/22645029
class SecurityGroupsCollection(Resource):

    def get(self):
        app.logger.debug('GET groups')
        mngr = mngr_api.Api(REGION)
        aws_groups = mngr.get_security_groups()

        app.logger.debug(aws_groups)
        cidrs = query_registered_cidrs()  # TODO: replace with persistence
        data = Marshaller.merge_records(cidrs, aws_groups)

        return data

        # NOTE: disabling marshalling
        # app.logger.debug('******* OUTPUT ************')
        # app.logger.debug('data: {0}'.format(data))
        # result = Marshaller._marshall_records_(data)
        # app.logger.debug('Result: {}'.format(, result))
        # return result


@api.route('/api/groups/<string:group_id>')
# Consider using flask_restful.marshal_with_fields - see:
#    http://stackoverflow.com/questions/22645029
class SecurityGroup(Resource):

    def get(self, group_id):

        app.logger.debug('GET group with {0}'.format(group_id))

        parts = group_id.split('-')
        assert parts[0] == 'sg'

        mngr = mngr_api.Api(REGION)
        aws_groups = mngr.get_security_groups(group_ids=[group_id])

        cidrs = query_registered_cidrs()
        data = Marshaller.merge_records(cidrs, aws_groups)

        return data


def query_registered_cidrs():

    # TODO: test for expiration? , expiration=DO_NOT_EXPIRE))
    return app.store.query_all()


# @cidrs_namespace.route('/')
@api.route('/cidr')
class SecurityGroupRule(Resource):

    @api.response(201, 'Rule successfully created.')
    def post(self):
        app.logger.debug('POST CIDR')

        # TODO: this is confused. Should be a CIDR, not rule?
        """Creates a new blog category."""
        mngr = mngr_api.Api(REGION)
        mngr.create_rule(request.json)
        return None, 201


@api.route('/api/rules/<string:group_id>')
class SecurityGroupRule(Resource):

    def get(self, group_id):
        app.logger.debug('Get rules for group_id')
        mngr = mngr_api.Api(REGION)
        aws_groups = mngr.get_security_groups(group_ids=[group_id])

        cidrs = query_registered_cidrs()
        data = Marshaller.merge_records(cidrs, aws_groups)

        return data


    # TODO: implement. Possibly replace with marshmallow due to deprecation?
    @api.response(201, 'Rule successfully updated.')
    def put(self, group_id):
        app.logger.debug('PUT? rule with group_id: {}'.format(group_id))



    @api.response(201, 'Rule successfully created.')
    def post(self, group_id):
        app.logger.debug('POST? rule with group_id: {}'.format(group_id))
        parts = group_id.split('-')
        assert parts[0] == 'sg'
        # help(self)
        # help(api)
        # Nope: request is not defined - print("request.__dict__:", request.__dict__)
        # Nope: request is not defined - print("request.form['data']:", request.form['data']
        app.logger.debug("group_id: {}".format(group_id))
        app.logger.debug("self.__dict__: {}".format(self.__dict__))
        app.logger.debug("api.payload: {}".format(api.payload))
        app.logger.debug("self.api.payload: {}".format(self.api.payload))
        app.logger.debug("api.__dict: {}".format(api.__dict__))
        app.logger.debug("app.__dict: {}".format(app.__dict__))
        app.logger.debug("self.api.__dict: {}".format(self.api.__dict__))
        post_body = self.api.payload # json.loads(request.data)

        app.logger.debug('POST rules to group {0}, data: {1}'.format(group_id, post_body))

        mngr = mngr_api.Api(REGION)
        sg_group = mngr.get_security_groups(group_ids=[group_id])[0]

        for curr in post_body:

            # TODO: validate cidr here or let Amazon handle that?
            cidr_str = curr['cidr']

            try:
                cidrs = mngr.get_registered_cidrs(cidr_str=cidr)[0]
            except IndexError:
                description = curr['description']
                owner = curr.get('owner')
                location = curr.get('location')
                cidr = registeredCidr.RegisteredCidr(
                    cidr=cidr_str, description=description, owner=owner,
                    location=location, expiration=RegisteredCidr.DO_NOT_EXPIRE)

            # Persist to store
            mngr.post_registered_cidr(cidr)

            protocol = curr.get('protocol', ALL_PROTOCOLS)
            from_port = curr['from_port']
            to_port = curr['to_port']
            expiration = curr.get('expiration', DO_NOT_EXPIRE)

            ingress_rule = awsSecurityGroup.IngressRule(
                protocol, from_port, to_port, cidr)

            mngr.authorize_ingress(sg_group, ingress_rule)

        cidrs = query_registered_cidrs()
        data = Marshaller.merge_records(cidrs, aws_groups)

        return data


@app.route('/testBoto')
def test_boto():

    app.logger.debug('testBoto')

    os.environ['BOTO_CONFIG'] = CONFIG_FILE

    session = boto3.session.Session()
    client = session.client(service_name='ec2', region_name=REGION)

    groups = AwsSecurityGroups.from_boto(client)

    # response = client.describe_security_groups()

    app.logger.debug(groups)
    return str(groups)

    # if response['ResponseMetadata']['HTTPStatusCode'] != 200:
    #     app.logger.error('Error getting SecurityGroup data from AWS:')
    #     app.logger.error(response['ResponseMetadata'])
    #     return

    # response['SecurityGroups']

    # client.authorize_security_group_egress(self, *args, **kwargs)

initialize_app()

if __name__ == '__main__':
    app.run(debug=True)
