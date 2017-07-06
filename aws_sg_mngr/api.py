# Check out github.com/awslabs/chalice !!!!
import boto3
import aws_sg_mngr.awsSecurityGroup

"""
TODO:
- Create a ~~~database abstraction layer, as well as a Redis (Elasticache) implementation~~~~ 
    no! Use a microservice!
  (for use at work, I need to figure out something else for my personal AWS account)
- Consider other persistence methods and create issues tagged "help wanted"
  See: https://sc5.io/posts/amazon-aws-lambda-data-caching-solutions-compared/#gref

- Also note Free Tier: DynamoDb 25GB on the permanent free tier (problem is, it's the slowest option)
  https://aws.amazon.com/s/dm/optimization/server-side-test/free-tier/free_np/

"""


class Api(object):

    def __init__(self, region):
        self.client = boto3.client(service_name='ec2', region_name=region)
       # aws_access_key_id=None, aws_secret_access_key=None,
       # aws_session_token=None, config=None):

    def get_security_groups(self):
        return aws_sg_mngr.awsSecurityGroup.AwsSecurityGroups.from_boto(self.client)

    def authorize_egress(self):
        #   response = client.authorize_security_group_egress(
        #       DryRun=TrueFalse,
        #       GroupId='string',
        #       SourceSecurityGroupName='string',
        #       SourceSecurityGroupOwnerId='string',
        #       IpProtocol='string',
        #       FromPort=123,
        #       ToPort=123,
        #       CidrIp='string',
        #       IpPermissions=[
        #           {
        #               'IpProtocol': 'string',
        #               'FromPort': 123,
        #               'ToPort': 123,
        #               'UserIdGroupPairs': [
        #                   {
        #                       'UserId': 'string',
        #                       'GroupName': 'string',
        #                       'GroupId': 'string',
        #                       'VpcId': 'string',
        #                       'VpcPeeringConnectionId': 'string',
        #                       'PeeringStatus': 'string'
        #                   },
        #               ],
        #               'IpRanges': [
        #                   {
        #                       'CidrIp': 'string'
        #                   },
        #               ],
        #               'Ipv6Ranges': [
        #                   {
        #                       'CidrIpv6': 'string'
        #                   },
        #               ],
        #               'PrefixListIds': [
        #                   {
        #                       'PrefixListId': 'string'
        #                   },
        #                       'PrefixListId': 'string'
        #                   },
        #               ]
        #           },
        #       ]
        #   )
        # :type DryRun: boolean
        # :param DryRun:
        pass

    def authorize_ingress(self, security_group, ingress_rule):
        """
            Request the addition of a new ingress rule in a security group

        """
        result = []
        response = self.client.authorize_security_group_ingress(
            # GroupName  # [EC2-Classic, default VPC] The name of the security group.
            IpProtocol=ingress_rule.protocol,  # The IP protocol name (tcp, udp, icmp) or number (see Protocol Numbers). (VPC only) Use -1 to specify all protocols. If you specify -1, or a protocol number other than tcp, udp, icmp, or 58 (ICMPv6), traffic on all ports is allowed, regardless of any ports you specify. For tcp, udp, and icmp, you must specify a port range. For protocol 58 (ICMPv6), you can optionally specify a port range; if you don't, traffic for all types and codes is allowed.
            CidrIp=ingress_rule.cidr,
            FromPort=ingress_rule.from_port,
            ToPort=ingress_rule.to_port,
            GroupId=security_group.group_id  # The ID of the security group. Required for a nondefault VPC.
            )  # The end of port range for the TCP and UDP protocols, or an ICMP/ICMPv6 code number. For the ICMP/ICMPv6 code number, use -1 to specify all codes.

# IpPermissions.N
# A set of IP permissions. Can be used to specify multiple rules in a single command.
# Type: Array of IpPermission objects
# Required: No

#   This function may be useful to expand ingress rules beyond CIDRs to security groups
#    def authorize_sg_ingress(self, security_group, ingress_rule):
# SourceSecurityGroupName
# [EC2-Classic, default VPC] The name of the source security group. You can't specify this parameter in combination with the following parameters: the CIDR IP address range, the start of the port range, the IP protocol, and the end of the port range. Creates rules that grant full ICMP, UDP, and TCP access. To create a rule with a specific IP protocol and port range, use a set of IP permissions instead. For EC2-VPC, the source security group must be in the same VPC.
# Type: String
# Required: No

# SourceSecurityGroupOwnerId
# [EC2-Classic] The AWS account number for the source security group, if the source security group is in a different account. You can't specify this parameter in combination with the following parameters: the CIDR IP address range, the IP protocol, the start of the port range, and the end of the port range. Creates rules that grant full ICMP, UDP, and TCP access. To create a rule with a specific IP protocol and port range, use a set of IP permissions instead.
# Type: String
# Required: No

        print(response);
        # if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        #     print('Error authorizing ingress from AWS:',)
        #     print(response['ResponseMetadata'])
        #     return None

        # TODO: ensure registered CIDR is recorded in DB?


        # for curr in response['SecurityGroups']:
        #     group = AwsSecurityGroup.Builder._from_SecurityGroups_item_(curr).build()
        #     result.append(group)

        # TODO: check this object for sensitive information?
        return response

        # authorize_security_group_ingress(self, *args, **kwargs)
        #   .. _Amazon VPC Limits: http://docs.aws.amazon.com/AmazonVPC/latest/UserGuide/VPC_Appendix_Limits.html
        #   .. _Protocol Numbers: http://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml

        # |  describe_security_grotsup_references(self, *args, **kwargs)
        # |      [EC2-VPC only] Describes the VPCs on the other side of a VPC peering connection that are referencing the security groups you've specified in this request.
        # |
        # |
        # |
        # |      See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/ec2-2016-11-15/DescribeSecurityGroupReferences>`_

        # |  describe_security_groups(self, *args, **kwargs)
        # |      .. _Protocol Numbers: http://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml
        # |      .. _Security Groups for Your VPC: http://docs.aws.amazon.com/AmazonVPC/latest/UserGuide/VPC_SecurityGroups.html
        # |      .. _Amazon EC2 Security Groups: http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-network-security.html
        # |
