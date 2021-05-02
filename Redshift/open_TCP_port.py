import boto3

DWH_PORT = ""

ec2 = boto3.client(
    "ec2",
    region_name="us-east-1",
    aws_access_key_id=str,
    aws_secret_access_key=str,
)

myClusterProps = ""

vpc = ec2.Vpc(id=myClusterProps["VpcId"])
defaultSg = list(vpc.security_groups.all())[0]
defaultSg.authorize_ingress(
    GroupName=defaultSg.group_name,
    CidrIp="0.0.0./0",
    IpProtocol="TCP",
    FromPort=int(DWH_PORT),
    ToPort=int(DWH_PORT),
)
