import boto3
import json

DWH_IAM_ROLE_NAME = ""

iam = boto3.client(
    "iam",
    region_name="us-east-1",
    aws_access_key_id=str,
    aws_secret_access_key=str,
)

dwhRole = iam.create_role(
    Path="/",
    RoleName=DWH_IAM_ROLE_NAME,
    Description="Allows Redshift clusters to call AWS services on your behalf.",
    AssumeRolePolicyDocument=json.dumps(
        {
            "Statement": [
                {
                    "Action": "sts:AssumeRole",
                    "Effect": "Allow",
                    "Principal": {"Service": "redshift.amazonaws.com"},
                }
            ],
            "Version": "2012-10-17",
        }
    ),
)

iam.attach_role_policy(
    RoleName=DWH_IAM_ROLE_NAME,
    PolicyArn="arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess",
)["ResponseMetadata"]["HTTPStatusCode"]
