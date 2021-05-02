import boto3

DWH_CLUSTER_TYPE = ""
DWH_NODE_TYPE = ""
DWH_NUM_NODES = ""
DWH_BD = ""
DWH_CLUSTER_IDENTIFIER = ""
DWH_DB_USER = ""
DWH_DB_PASSWORD = ""
roleArn = []

redshift = boto3.client(
    "redshift",
    region_name="us-east-1",
    aws_access_key_id=str,
    aws_secret_access_key=str,
)

response = redshift.create_cluster(
    # HW
    ClusterType=DWH_CLUSTER_TYPE,
    NodeType=DWH_NODE_TYPE,
    NumberOfNodes=int(DWH_NUM_NODES),
    # Identifiers & Credentials
    DBName=DWH_BD,
    ClusterIdentifier=DWH_CLUSTER_IDENTIFIER,
    MasterUserName=DWH_DB_USER,
    MasterUserPassword=DWH_DB_PASSWORD,
    # Roles (for s3 access)
    IamRoles=[roleArn],
)
