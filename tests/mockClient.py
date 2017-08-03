import json


class MockClient(object):

    def __init__(self):
        """ Set up the initial state of the client """
        with open('tests/example-security-group.txt', 'r') as testfile:
            self.sg_data = json.load(testfile)

    def describe_security_groups(self, GroupIds=None):
        response = self.sg_data

        # GroupIds filtering
        if GroupIds is not None:
            idx = 0
            groups = response['SecurityGroups']
            while len(groups) > 0 and idx < len(groups):
                if groups[idx]['GroupId'] not in GroupIds:
                    del response['SecurityGroups'][idx]
                else:
                    idx += 1

        response['ResponseMetadata'] = {}
        response['ResponseMetadata']['HTTPStatusCode'] = 200

        return response

    def authorize_security_group_ingress(
            self, GroupId, IpProtocol, CidrIp, FromPort, ToPort):
            # GroupName  # [EC2-Classic, default VPC] The name of the
            # security group.

        for idx in range(len(self.sg_data['SecurityGroups'])):
            if self.sg_data['SecurityGroups'][idx]['GroupId'] != GroupId:
                continue

            print(idx, self.sg_data['SecurityGroups'][idx]['GroupId'], 
                self.sg_data['SecurityGroups'][idx]['Description'], '\n',
                self.sg_data['SecurityGroups'][idx]['IpPermissions'])

            # Test to see if an IpPermissions group exists for the from & to ports
            for perm_idx in range(len(self.sg_data['SecurityGroups'][idx]['IpPermissions'])):
                if(self.sg_data['SecurityGroups'][idx]['IpPermissions'][perm_idx]['FromPort'] == FromPort and
                   self.sg_data['SecurityGroups'][idx]['IpPermissions'][perm_idx]['ToPort'] == ToPort and
                   self.sg_data['SecurityGroups'][idx]['IpPermissions'][perm_idx]['IpProtocol'] == IpProtocol):

                    # Finally, check if this Cidr is already in the IpRanges list
                    for curr_cidr in self.sg_data['SecurityGroups'][idx]['IpPermissions'][perm_idx]['IpRanges']:
                        if curr_cidr['CidrIp'] == CidrIp:
                            return True

                    # Otherwise, this is a new one we need to include                                
                    self.sg_data['SecurityGroups'][idx]['IpPermissions'][perm_idx]['IpRanges'].append({'CidrIp': CidrIp})
                    return True


            # This is the right security group, but we need a new IpPermissions item:
            new_ip_permission = {
                "PrefixListIds": [], 
                "FromPort": FromPort, 
                "IpRanges": [{"CidrIp": CidrIp}],
                "ToPort": ToPort, 
                "IpProtocol": IpProtocol, 
                "UserIdGroupPairs": [], 
                "Ipv6Ranges": []
            }

            self.sg_data['SecurityGroups'][idx]['IpPermissions'].append(new_ip_permission)
            return True

        # We did not find a matching security group. This is an error.
        return False
