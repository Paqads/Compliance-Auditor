import boto3
from config.settings import settings

class AWSClient:
    def __init__(self):
        self.ec2 = boto3.client('ec2', region_name=settings.AWS_REGION)
        self.s3 = boto3.client('s3')
        # Add other AWS services as needed

aws_client = AWSClient()