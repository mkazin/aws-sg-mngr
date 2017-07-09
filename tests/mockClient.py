import json


class MockClient(object):

    def describe_security_groups(self, GroupIds=None):
        with open('tests/example-security-group.txt', 'r') as testfile:
            security_groups_response = json.load(testfile)

        # GroupIds filtering
        if GroupIds is not None:
            idx = 0
            groups = security_groups_response['SecurityGroups']
            while len(groups) > 0 and idx < len(groups):
                if groups[idx]['GroupId'] not in GroupIds:
                    del security_groups_response['SecurityGroups'][idx]
                else:
                    idx += 1

        security_groups_response['ResponseMetadata'] = {}
        security_groups_response['ResponseMetadata']['HTTPStatusCode'] = 200

        return security_groups_response

    def authorize_security_group_ingress(
            self, GroupId, IpProtocol, CidrIp, FromPort, ToPort):
            # GroupName  # [EC2-Classic, default VPC] The name of the
            # security group.

        return True
