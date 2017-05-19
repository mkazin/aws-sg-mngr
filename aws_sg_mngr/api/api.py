Check out github.com/awslabs/chalice !!!!

"""
TODO:
- Create a database abstraction layer, as well as a Redis (Elasticache) implementation
  (for use at work, I need to figure out something else for my personal AWS account)
- Consider other persistence methods and create issues tagged "help wanted" 
  See: https://sc5.io/posts/amazon-aws-lambda-data-caching-solutions-compared/#gref
  
- Also note Free Tier: DynamoDb 25GB on the permanent free tier (problem is, it's the slowest option)
  https://aws.amazon.com/s/dm/optimization/server-side-test/free-tier/free_np/

"""




    def authorize_egress(self, client):
        pass
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


    def authorize_ingress(self, client):
        pass
        # authorize_security_group_ingress(self, *args, **kwargs)
        #   .. _Amazon VPC Limits: http://docs.aws.amazon.com/AmazonVPC/latest/UserGuide/VPC_Appendix_Limits.html
        #   .. _Protocol Numbers: http://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml



 # |  describe_security_group_references(self, *args, **kwargs)
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
