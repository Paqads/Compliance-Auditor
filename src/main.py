import asyncio
import json
import logging
from datetime import datetime
from aws_compliance import AwsComplianceAuditor
from azure_compliance import AzureComplianceAuditor

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='compliance_audit.log'
)

async def generate_report():
    start_time = datetime.now()
    report = {
        'timestamp': start_time.isoformat(),
        'aws': {},
        'azure': {},
        'overall_status': 'COMPLIANT'
    }
    
    try:
        aws_auditor = AwsComplianceAuditor(region='us-east-1')
        azure_auditor = AzureComplianceAuditor(subscription_id='your-subscription-id')
        
        aws_results, azure_results = await asyncio.gather(
            aws_auditor.check_encryption(),
            azure_auditor.check_encryption()
        )
        
        report['aws'] = aws_results
        report['azure'] = azure_results
        report['overall_status'] = 'COMPLIANT' if (
            aws_results['overall'] == 'COMPLIANT' and 
            azure_results['overall'] == 'COMPLIANT'
        ) else 'NON_COMPLIANT'
        
    except Exception as e:
        logging.error(f"Audit failed: {str(e)}")
        report['overall_status'] = 'ERROR'
    
    report['execution_time'] = (datetime.now() - start_time).total_seconds()
    
    filename = f"compliance_report_{start_time.strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"Report generated: {filename}")
    return report

if __name__ == "__main__":
    asyncio.run(generate_report())