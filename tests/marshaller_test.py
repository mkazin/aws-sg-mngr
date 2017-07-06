import json
import pytest
import aws_sg_mngr
import aws_sg_mngr.registeredCidr
import aws_sg_mngr.awsSecurityGroup
import aws_sg_mngr.marshaller
from aws_sg_mngr.marshaller import Marshaller



def test_merge():
    print('========= test_merge =========')
    cidrs = get_registered_cidrs()

    print('cidrs: {0}'.format(','.join(str(x) for x in cidrs)))
    sgs = [get_test_sg()]
    print('sgs: {0}'.format(str(sgs[0])))

    data = Marshaller.merge_records(cidrs, sgs)

    assert data[0]['GroupId'] == 'sg-ebe1ac8f'
    assert data[0]['GroupName'] == 'Elasticsearch'


# def test_functionality():
#     from flask_restful import fields, marshal

#     inner_fields = {
#         'CidrIp': fields.String, 
#         'FromPort': fields.Integer, 
#         'ToPort': fields.Integer, 
#         'IpProtocol': fields.String,
#         'Owner': fields.String,
#         'Descripion': fields.String
#     }

#     data = [
#         {
#         'CidrIp': 'CIDR A', 
#         'FromPort': 22, 
#         'ToPort': 22, 
#         'IpProtocol': 'tcp',
#         'Owner': 'mkazin',
#         'Descripion': 'first cidr'
#         },
#         {
#         'CidrIp': 'CIDR B', 
#         'FromPort': 9200, 
#         'ToPort': 9200, 
#         'IpProtocol': 'tcp',
#         'Owner': 'mkazin',
#         'Descripion': 'second cidr'
#         }        
#         ]

#     # resource_fields = {
#     #     'GroupId': fields.String, 
#     #     'OwnerId': fields.String, 
#     #     'GroupName': fields.String,
#     #     'Rules': fields.List(fields.Nested(rule_fields))
#     # }

#     # merged_fields = fields.List(fields.Nested(resource_fields))
#     # merged_fields = {'Rules': fields.List(fields.Nested(resource_fields))}
#     result = marshal(data, inner_fields)

#     print('Result: {}'.format(result))
#     assert hasattr(result, 'rules')
#     assert False

def test_marshalling():
    # TODO: remove exit
    return
    print('========= test_marshalling =========')

    cidrs = get_registered_cidrs()

    print('******* MERGING ************')
    print('1) cidrs: {0}'.format(','.join(str(x) for x in cidrs)))
    sgs = [get_test_sg()]
    print('2) sgs: {0}'.format(str(sgs[0])))

    data = Marshaller.merge_records(cidrs, sgs)

    print('******* OUTPUT ************')
    print('data: {0}'.format(data))
    result = Marshaller._marshall_records_(data)

    print('result: {0}'. format(result))
    assert hasattr(result, 'rules')

    # rule_fields = {
    #     'CidrIp': fields.String, 
    #     'FromPort': fields.Integer, 
    #     'ToPort': fields.Integer, 
    #     'IpProtocol': fields.String
    # }

    # expected_result = {
    #     'GroupId': fields.String, 
    #     'OwnerId': fields.String, 
    #     'GroupName': fields.String,
    #         'Rules': [
    #         {               
    #             'CidrIp': fields.String, 
    #             'FromPort': fields.Integer, 
    #             'ToPort': fields.Integer, 
    #             'IpProtocol': fields.String
    #         }, {
    #             'CidrIp': fields.String, 
    #             'FromPort': fields.Integer, 
    #             'ToPort': fields.Integer, 
    #             'IpProtocol': fields.String
    #         }
    #         ]
    # }



def get_test_sg():

    with open('tests/example-security-group.txt', 'r') as testfile:
        contents = testfile.read()

    security_groups_response = json.loads(contents)
    group_data = security_groups_response["SecurityGroups"][0]

    builder = aws_sg_mngr.awsSecurityGroup.AwsSecurityGroup.Builder._from_SecurityGroups_item_(group_data)
    # sg = builder.build()

    # builder = aws_sg_mngr.awsSecurityGroup.AwsSecurityGroup.Builder()
    # builder.withGroupName('Elasticsearch')
    # # result['VpcId'] = group['VpcId']
    # builder.withOwnerId('709761231924')
    # builder.withGroupId('sg-ebe1ac8f')
    # builder.withDescription("Created for Elasticsearch 2015-04-21T12:49:28.513-04:00")

    # builder.withTags([{"Value": "Elasticsearch", "Key": "Name"}])

    # egress_list = [
    #             {
    #                 "IpProtocol": "-1", 
    #                 "PrefixListIds": [], 
    #                 "IpRanges": [
    #                     {
    #                         "CidrIp": "0.0.0.0/0"
    #                     }
    #                 ], 
    #                 "UserIdGroupPairs": [], 
    #                 "Ipv6Ranges": []
    #             }
    #         ]

    # ingress_list = [
    #             {
    #                 "PrefixListIds": [], 
    #                 "FromPort": 22, 
    #                 "IpRanges": [
    #                     {
    #                         "CidrIp": "209.6.205.245/32"
    #                     }, 
    #                     {
    #                         "CidrIp": "209.6.37.244/32"
    #                     }
    #                 ], 
    #                 "ToPort": 22, 
    #                 "IpProtocol": "tcp", 
    #                 "UserIdGroupPairs": [], 
    #                 "Ipv6Ranges": []
    #             }]

    # builder.withRuleList(builder.withEgressRule, egress_list)
    # builder.withRuleList(builder.withIngressRule, ingress_list)

    return builder.build()

def get_registered_cidrs():
    cidrs = []
    cidrs.append(aws_sg_mngr.registeredCidr.RegisteredCidr("50.187.58.239/32", "Home", owner="mjkazin", location="Home")) # TODO: test expiration:: , expiration=DO_NOT_EXPIRE))
    cidrs.append(aws_sg_mngr.registeredCidr.RegisteredCidr("75.67.236.14/32", "Company HQ", owner="mjkazin", location="Office")) # TODO: test expiration:: , expiration=DO_NOT_EXPIRE))
    return cidrs
