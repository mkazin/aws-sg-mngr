from flask import Flask
from flask_restful import fields, marshal
from registeredCidr import RegisteredCidr
from awsSecurityGroup import AwsSecurityGroups
import json
import boto3
from botocore.exceptions import NoCredentialsError

import logging
from logging.handlers import RotatingFileHandler

# TODO: remove when I'm no longer setting environment variable for testing
import os
app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)
file_handler = RotatingFileHandler('flask.log', maxBytes=1024 * 1024 * 100, backupCount=3)
file_handler.setLevel(logging.DEBUG)
app.logger.addHandler(file_handler)


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

def find_mngr_sg(sgs, cidr):
    for curr in sgs:
        if curr.matches(cidr):
            return curr
    return None

def merge_records(mngr_sgs, aws_sgs):
    print '=========================================================='
    print '==================== Merging here ========================'
    print '=========================================================='
    merged = []
    print 'aws_sgs: ', aws_sgs
    for aws_group in aws_sgs['SecurityGroups']:
        print '=========================================================='
        print 'aws_group: ', json.dumps(aws_group)


        # Doc references for AWS Security Group:
        # http://docs.aws.amazon.com/cli/latest/reference/ec2/describe-security-groups.html
        curr = {}
        curr['GroupId'] = aws_group['GroupId']
        curr['OwnerId'] = aws_group['OwnerId']
        curr['GroupName'] = aws_group['GroupName']
        curr['Rules'] = []

        for permission in aws_group['IpPermissions']:
            print 'permission: ', permission
            base_rule = {}
            base_rule['FromPort'] = permission['FromPort']
            base_rule['ToPort'] = permission['ToPort']
            base_rule['IpProtocol'] = permission['IpProtocol']

            for cidr in permission['IpRanges']:
                print 'cidr', cidr[u'CidrIp']
                rule = base_rule
                rule['CidrIp'] = cidr[u'CidrIp']

                mngr_group = find_mngr_sg(mngr_sgs, cidr['CidrIp'])
                #cidr_info = {}
                if mngr_group is not None:
                    print '!!!!!! matching mngr_group:', mngr_group
                    rule['Owner'] = mngr_group.owner
                    rule['Description'] = mngr_group.description
                    curr['Rules'].append(rule)

                #rule['CidrInfo'] = cidr_info
        merged.append(curr)
    print '\n=========================================================='
    return merged



def marshall_records(data):
    # TODO: these should be constant, no need to build/allocate at runtime
    #resource_fields = {'name': fields.String, 'first_names': fields.List(fields.String)}

    rule_fields = {
        'CidrIp': fields.String, 
        'FromPort': fields.Integer, 
        'ToPort': fields.Integer, 
        'IpProtocol': fields.String
    }

    resource_fields = {
        'GroupId': fields.String, 
        'OwnerId': fields.String, 
        'GroupName': fields.String,
        'Rules': fields.List(fields.Nested(rule_fields))
    }

    merged_fields = fields.List(fields.Nested(resource_fields))

    marshalled = marshal(data, merged_fields)
    print "Marshalled: ", marshalled

    return json.dumps(marshalled, sort_keys=True, indent=4, separators=(',', ': '))
    #'{"first_names": ["Emile", "Raoul"], "name": "Bougnazal"}'


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


