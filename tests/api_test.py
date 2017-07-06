from aws_sg_mngr import api as asmapi
from aws_sg_mngr import awsSecurityGroup
from aws_sg_mngr import registeredCidr

import json


class MockClient(object):

    def describe_security_groups(self):
        with open('tests/example-security-group.txt', 'r') as testfile:
            security_groups_response = json.load(testfile)

        security_groups_response['ResponseMetadata'] = {}
        security_groups_response['ResponseMetadata']['HTTPStatusCode'] = 200

        return security_groups_response

    def authorize_security_group_ingress(
            self, GroupId, IpProtocol, CidrIp, FromPort, ToPort):
            # GroupName  # [EC2-Classic, default VPC] The name of the
            # security group.

        return True


def test_get_security_groups():
    api = asmapi.Api('us-east-1')
    api.client = MockClient()

    groups = api.get_security_groups()

    sg = groups.groups[0]
    assert sg is not None
    assert 'Created for Elasticsearch' in sg.description
    assert sg.group_id == 'sg-ebe1ac8f'
    assert sg.group_name == 'Elasticsearch'

    # for rule in sg.egress_rules:
    #     print("- Egress rule: {}".format(str(rule)))
    # for rule in sg.ingress_rules:
    #     print("+ Ingress rule: {}".format(str(rule)))

    assert len(sg.egress_rules) == 1
    assert sg.egress_rules[0].protocol == awsSecurityGroup.ALL_PROTOCOLS
    assert sg.egress_rules[0].cidr == "0.0.0.0/0"

    assert len(sg.ingress_rules) == 9
    assert sg.ingress_rules[0].protocol == 'tcp'
    assert sg.ingress_rules[0].cidr == "209.6.205.245/32"
    assert sg.ingress_rules[0].from_port == 22
    assert sg.ingress_rules[0].to_port == 22

    my_cidr = registeredCidr.RegisteredCidr("192.168.0.42/32", "Test CIDR", owner="AWS-SG-MNGR", location="/tests/")

    new_ingress_rule = awsSecurityGroup.IngressRule('tcp', '22', '22', my_cidr)

    response = api.authorize_ingress(security_group=sg, ingress_rule=new_ingress_rule)
    assert response
