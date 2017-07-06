import json
import flask_restful
from flask_restful import fields, marshal


class Marshaller(object):
    """ Handle the merging and marshalling of AWS and aws_sg_mngr
        records into our API format

    """

    @staticmethod
    def merge_records(mngr_sgs, aws_sgs):
        print('==========================================================')
        print('==================== Merging here ========================')
        print('==========================================================')
        result = []

        if type(aws_sgs) == list:
            groups = aws_sgs
        else:
            groups = aws_sgs.groups

        print("Merging aws_sgs:")
        print('\n'.join('\t- {0}'.format(str(x)) for x in groups))

        print("With mngr_sgs:")
        print('\n'.join('\t- {0}'.format(str(x)) for x in mngr_sgs))

        for aws_group in groups:
            print('==========================================================')
            print('\n\t\t- Current aws_group: {0}'.format(aws_group))

            # Doc references for AWS Security Group:
            # http://docs.aws.amazon.com/cli/latest/reference/ec2/describe-security-groups.html
            merged_rule = {}
            merged_rule['GroupId'] = aws_group.group_id
            # merged_rule['OwnerId'] = aws_group.owner_id
            merged_rule['GroupName'] = aws_group.group_name
            merged_rule['Rules'] = []

            for curr_rule in aws_group.egress_rules + aws_group.ingress_rules:
                # print('\t\t\t- Current rule: {0}'.format(curr_rule))
                base_rule = {}

                base_rule['IpProtocol'] = curr_rule.protocol
                base_rule['Cidr'] = curr_rule.cidr

                try:
                    base_rule['FromPort'] = curr_rule.from_port
                    base_rule['ToPort'] = curr_rule.to_port

                except AttributeError:
                    # This is fine. We don't have these attributes on EgressRules
                    pass

                # print('cidr {0}'.format(curr_rule.cidr))
                rule = base_rule

                mngr_group = find_mngr_sg(mngr_sgs, curr_rule.cidr)
                # cidr_info = {}
                if mngr_group is not None:
                    print('\t\t\t Found matching mngr_group: {0}'.format(mngr_group))
                    print('\t\t\t\t for current rule: {0}'.format(curr_rule))

                    rule['Owner'] = mngr_group.owner
                    rule['Description'] = mngr_group.description
                    merged_rule['Rules'].append(rule)

                    # rule['CidrInfo'] = cidr_info
            print('\t\t merged_rule: {0}'.format(merged_rule))
            result.append(merged_rule)
        print('\n==========================================================')
        return result

    @staticmethod
    def _marshall_records_(data):
        """
        Rule ==> {
            'CidrIp': fields.String,
            'FromPort': fields.Integer,
            'ToPort': fields.Integer,
            'IpProtocol': fields.String
        }

        Resource ==> {
            'GroupId': fields.String,
            'OwnerId': fields.String,
            'GroupName': fields.String,
            'Rules': fields.List(fields.Nested(Rule))
        }
        """
        # TODO: these should be constant, no need to build/allocate at runtime
        # resource_fields = {'name': fields.String, 'first_names': fields.List(fields.String)}

        rule_fields = {
            'CidrIp': fields.String,
            'FromPort': fields.Integer,
            'ToPort': fields.Integer,
            'IpProtocol': fields.String,
            'Owner': fields.String,
            'Descripion': fields.String
        }

        resource_fields = {
            'GroupId': fields.String,
            'OwnerId': fields.String,
            'GroupName': fields.String,
            'Rules': fields.List(fields.Nested(rule_fields))
        }

        # merged_fields = fields.List(fields.Nested(resource_fields))
        merged_fields = {'Rules': fields.List(fields.Nested(resource_fields))}

        print('data: {0}'.format(data))
        marshalled = marshal(data, merged_fields)
        print("Marshalled: {0}".format(marshalled))

        return json.dumps(marshalled, sort_keys=True, indent=4, separators=(',', ': '))
        # '{"first_names": ["Emile", "Raoul"], "name": "Bougnazal"}'


def find_mngr_sg(sgs, cidr):
    for curr in sgs:
        # print('Comparing {0} to {1}'.format(curr.cidr, cidr))
        if curr.cidr == cidr:
            return curr
    return None
