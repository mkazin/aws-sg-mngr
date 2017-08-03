from aws_sg_mngr import api as asmapi
from aws_sg_mngr import awsSecurityGroup
from aws_sg_mngr import registeredCidr
from tests.mockClient import MockClient

import json


def test_get_security_groups():
    api = asmapi.Api('us-east-1')
    api.client = MockClient()

    groups = api.get_security_groups()

    sg = groups[0]
    assert sg is not None
    assert 'Created for Elasticsearch' in sg.description
    assert sg.group_id == 'sg-ebe1ac8f'
    assert sg.group_name == 'Elasticsearch'

    # for rule in sg.egress_rules:
    #     print("- Egress rule: {0}".format(str(rule)))
    # for rule in sg.ingress_rules:
    #     print("+ Ingress rule: {0}".format(str(rule)))

    assert len(sg.egress_rules) == 1
    assert sg.egress_rules[0].protocol == awsSecurityGroup.ALL_PROTOCOLS
    assert sg.egress_rules[0].cidr == "0.0.0.0/0"

    assert len(sg.ingress_rules) == 9
    assert sg.ingress_rules[0].protocol == 'tcp'
    assert sg.ingress_rules[0].cidr == "209.6.205.245/32"
    assert sg.ingress_rules[0].from_port == 22
    assert sg.ingress_rules[0].to_port == 22


def test_get_single_security_group():

    api = asmapi.Api('us-east-1')
    api.client = MockClient()

    groups = api.get_security_groups(group_ids=['sg-ebe1ac8f'])
    sg = groups[0]
    assert sg is not None
    assert 'Created for Elasticsearch' in sg.description
    assert sg.group_id == 'sg-ebe1ac8f'
    assert sg.group_name == 'Elasticsearch'

    # for rule in sg.egress_rules:
    #     print("- Egress rule: {0}".format(str(rule)))
    # for rule in sg.ingress_rules:
    #     print("+ Ingress rule: {0}".format(str(rule)))

    assert len(sg.egress_rules) == 1
    assert sg.egress_rules[0].protocol == awsSecurityGroup.ALL_PROTOCOLS
    assert sg.egress_rules[0].cidr == "0.0.0.0/0"

    assert len(sg.ingress_rules) == 9
    assert sg.ingress_rules[0].protocol == 'tcp'
    assert sg.ingress_rules[0].cidr == "209.6.205.245/32"
    assert sg.ingress_rules[0].from_port == 22
    assert sg.ingress_rules[0].to_port == 22


def test_authorize_ingress():

    # Get the test security group
    api = asmapi.Api('us-east-1')
    api.client = MockClient()
    groups = api.get_security_groups(group_ids=['sg-ebe1ac8f'])
    sg = groups[0]
    assert sg is not None
    assert sg.group_id == 'sg-ebe1ac8f'
    assert sg.group_name == 'Elasticsearch'

    # Request ingress
    protocol = 'tcp'
    from_port = 1234
    to_port = 5678
    cidr = '12.34.56.78/32'
    ingress_rule = awsSecurityGroup.IngressRule(protocol, from_port, to_port, cidr)
    api.authorize_ingress(security_group=sg, ingress_rule=ingress_rule)

    # Request the security group, expect to see the added rule
    groups = api.get_security_groups(group_ids=['sg-ebe1ac8f'])

    found = False

    for curr_group in groups:
        print('Searching for {}'.format(ingress_rule))
        for curr_rule in curr_group.ingress_rules:
            print('   Testing {}'.format(curr_rule))
            if curr_rule == ingress_rule:
                print('    Found!!')
                found = True

    # assert ingress_rule in curr_group.ingress_rules
    assert found

    # my_cidr = registeredCidr.RegisteredCidr(
    #     "192.168.0.42/32", "Test CIDR", owner="AWS-SG-MNGR", location="/tests/")

    # new_ingress_rule = awsSecurityGroup.IngressRule('tcp', '22', '22', my_cidr)

    # response = api.authorize_ingress(security_group=sg, ingress_rule=new_ingress_rule)
    # assert response
