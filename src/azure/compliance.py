from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.storage import StorageManagementClient
from typing import Dict, Any
import logging
from concurrent.futures import ThreadPoolExecutor
import asyncio

class AzureComplianceAuditor:
    def __init__(self, subscription_id: str):
        self.subscription_id = subscription_id
        self.credential = DefaultAzureCredential()
        self.executor = ThreadPoolExecutor(max_workers=5)
        self.logger = logging.getLogger('azure_compliance')

    async def check_encryption(self) -> Dict[str, Any]:
        """Check all Azure encryption compliance"""
        try:
            loop = asyncio.get_event_loop()
            disk_task = loop.run_in_executor(self.executor, self._check_disk_encryption)
            storage_task = loop.run_in_executor(self.executor, self._check_storage_encryption)
            disk_results, storage_results = await asyncio.gather(disk_task, storage_task)
            
            return {
                'disks': disk_results,
                'storage': storage_results,
                'overall': 'COMPLIANT' if all(r['compliance_status'] == 'COMPLIANT' 
                                            for r in [disk_results, storage_results]) 
                          else 'NON_COMPLIANT'
            }
        except Exception as e:
            self.logger.error(f"Azure encryption check failed: {str(e)}")
            raise

    def _check_disk_encryption(self) -> Dict[str, Any]:
        """Check disk encryption status"""
        compute_client = ComputeManagementClient(self.credential, self.subscription_id)
        disks = list(compute_client.disks.list())
        encrypted = sum(1 for disk in disks if disk.encryption is not None)
        
        return {
            'encrypted': encrypted,
            'total': len(disks),
            'compliance_status': 'COMPLIANT' if encrypted == len(disks) else 'NON_COMPLIANT'
        }

    def _check_storage_encryption(self) -> Dict[str, Any]:
        """Check storage account encryption"""
        storage_client = StorageManagementClient(self.credential, self.subscription_id)
        accounts = list(storage_client.storage_accounts.list())
        encrypted = sum(1 for acc in accounts if acc.encryption.services.blob.enabled)
        
        return {
            'encrypted': encrypted,
            'total': len(accounts),
            'compliance_status': 'COMPLIANT' if encrypted == len(accounts) else 'NON_COMPLIANT'
        }

    def __del__(self):
        self.executor.shutdown(wait=False)