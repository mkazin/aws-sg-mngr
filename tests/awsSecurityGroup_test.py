import json
from aws_sg_mngr import awsSecurityGroup


def test_mock_boto():
    # TODO: implement
    pass


def test_build():
    # TODO: implement
    pass


def test_deserialize():

    with open('tests/example-security-group.txt', 'r') as testfile:
        contents = testfile.read()

    security_groups_response = json.loads(contents)
    group_data = security_groups_response["SecurityGroups"][0]

    builder = awsSecurityGroup.AwsSecurityGroup.Builder._from_SecurityGroups_item_(group_data)
    sg = builder.build()

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
