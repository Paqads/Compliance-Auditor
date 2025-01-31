import boto3
import logging
from typing import Dict, Any
from concurrent.futures import ThreadPoolExecutor
import asyncio

class AwsComplianceAuditor:
    def __init__(self, region: str = 'us-east-1'):
        self.region = region
        self.ec2 = boto3.client('ec2', region_name=region)
        self.s3 = boto3.client('s3')
        self.executor = ThreadPoolExecutor(max_workers=5)
        self.logger = logging.getLogger('aws_compliance')

    async def check_encryption(self) -> Dict[str, Any]:
        """Check all AWS encryption compliance"""
        try:
            loop = asyncio.get_event_loop()
            ebs_task = loop.run_in_executor(self.executor, self._check_ebs_encryption)
            s3_task = loop.run_in_executor(self.executor, self._check_s3_encryption)
            ebs_results, s3_results = await asyncio.gather(ebs_task, s3_task)
            
            return {
                'ebs': ebs_results,
                's3': s3_results,
                'overall': 'COMPLIANT' if all(r['compliance_status'] == 'COMPLIANT' 
                                            for r in [ebs_results, s3_results]) 
                          else 'NON_COMPLIANT'
            }
        except Exception as e:
            self.logger.error(f"AWS encryption check failed: {str(e)}")
            raise

    def _check_ebs_encryption(self) -> Dict[str, Any]:
        """Check EBS volume encryption"""
        paginator = self.ec2.get_paginator('describe_volumes')
        encrypted = 0
        total = 0
        
        for page in paginator.paginate():
            volumes = page['Volumes']
            total += len(volumes)
            encrypted += sum(1 for vol in volumes if vol.get('Encrypted', False))
            
        return {
            'encrypted': encrypted,
            'total': total,
            'compliance_status': 'COMPLIANT' if encrypted == total else 'NON_COMPLIANT'
        }

    def _check_s3_encryption(self) -> Dict[str, Any]:
        """Check S3 bucket encryption"""
        buckets = self.s3.list_buckets()['Buckets']
        encrypted = 0
        
        for bucket in buckets:
            try:
                self.s3.get_bucket_encryption(Bucket=bucket['Name'])
                encrypted += 1
            except self.s3.exceptions.ClientError as e:
                if e.response['Error']['Code'] == 'ServerSideEncryptionConfigurationNotFoundError':
                    continue
                raise
        
        return {
            'encrypted': encrypted,
            'total': len(buckets),
            'compliance_status': 'COMPLIANT' if encrypted == len(buckets) else 'NON_COMPLIANT'
        }

    def __del__(self):
        self.executor.shutdown(wait=False)