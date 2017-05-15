from flask import Flask
from flask_restplus import Resource, Api
from flast_restful_swagger import swagger
from flask_restful import fields, marshal
from registeredCidr import RegisteredCidr
from awsSecurityGroup import AwsSecurityGroups
import json
import boto3
from botocore.exceptions import NoCredentialsError
import .marshaller

import logging
from logging.handlers import RotatingFileHandler

# TODO: remove when I'm no longer setting environment variable for testing
import os
app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)
file_handler = RotatingFileHandler('flask.log', maxBytes=1024 * 1024 * 100, backupCount=3)
file_handler.setLevel(logging.DEBUG)
app.logger.addHandler(file_handler)

# Set up the flast_restplus API
# See http://michal.karzynski.pl/blog/2016/06/19/building-beautiful-restful-apis-using-flask-swagger-ui-flask-restplus/
api = Api(app)

# Set up Swagger Docs
# See http://github.com/rantav/flask-restful-swagger
# NOTE: this may not be needed. See if flask_restplus already provides this
#api = swagger.docs(Api(app), apiVersion='0.1')

CONFIG_FILE='server/config/boto.cfg'
REGION = 'us-east-1'

@app.route('/')
def hello_world():
    #return 'Hello, World!'

# Merge our data into AWS' .  For more see:
#   https://flask-restful.readthedocs.io/en/0.3.5/fields.html#complex-structures


    with open('server/example-security-group.txt', 'r') as stub_group:
        aws_groups = json.load(stub_group)


    mngr_records = [
        RegisteredCidr('209.6.205.245/32', 'Mike home', owner='mike', location='Somerville, MA', expiration=RegisteredCidr.DO_NOT_EXPIRE),
        RegisteredCidr('96.95.188.89/32', 'LinkeDrive HQ', owner='mike', location='11 Elkins St. Boston, MA', expiration=RegisteredCidr.DO_NOT_EXPIRE)

        # {'CidrIp': '209.6.205.245/32', 'Owner': 'mike', 'Description': 'Mike home', 'Location': 'Somerville, MA', 'DoNotDelete': True}
    ]
#        mngr_cidr = next((x for x in mngr_sgs if x['CidrIp'] == curr['CidrIp']), None)
#        cidr_info = {}
#        if mngr_group is not None:
#            cidr_info['Owner'] = mngr_cidr['Owner']
#            cidr_info['Description'] = mngr_cidr['Description']

# Top of the CIDR spreadsheet...
#Priority	CIDR	Location	Service	Owner	Comments	Old values
#A	96.95.188.89/32	11 Elkins, Boston MA	(Mechanic Advisor)	LinkeDrive HQ	Should probably get a VPN set up
#B	108.20.118.134/32 	Reading, MA		Hoyt home	please ask me before you delete
#B	209.6.205.245/32	Somerville, MA	RCN	Mike Home	Do not delete
#B	24.61.216.61/32			JD - unknown																								

    merged = merge_records(mngr_records, aws_groups)
    print 'Merged:', merged
    marshalled = marshall_records(merged)
    return marshalled
    #json.dumps(marshalled, sort_keys=True, indent=4, separators=(',', ': '))
    
    #return json.dumps(groups)



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

    print groups
    return str(groups)

    # if response['ResponseMetadata']['HTTPStatusCode'] != 200:
    #     print 'Error getting SecurityGroup data from AWS:',
    #     print response['ResponseMetadata']
    #     return
    
    # response['SecurityGroups']

    # client.authorize_security_group_egress(self, *args, **kwargs)


