<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">    
</head>
<body>

<h1>Cloud Compliance Audit Tool</h1>

<p>
    <span class="badge badge-blue">Cloud: AWS | Azure</span>
    <span class="badge badge-green">Python: 3.8+</span>
</p>

<p>A robust solution for auditing encryption compliance across AWS and Azure cloud environments, aligned with NIST security controls.</p>

<h2>Table of Contents</h2>
<ul>
    <li><a href="#project-overview">Project Overview</a></li>
    <li><a href="#key-features">Key Features</a></li>
    <li><a href="#use-case-scenarios">Use Case Scenarios</a></li>
    <li><a href="#installation">Installation</a></li>
    <li><a href="#configuration">Configuration</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#report-structure">Report Structure</a></li>
    <li><a href="#extending-the-tool">Extending the Tool</a></li>
    <li><a href="#troubleshooting">Troubleshooting</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
</ul>

<h2 id="project-overview">Project Overview</h2>
<p>This tool provides automated compliance checks for:</p>
<ul>
    <li><strong>AWS Resources</strong>
        <ul>
            <li>EBS Volume Encryption (NIST AC-3, SC-13)</li>
            <li>S3 Bucket Encryption</li>
        </ul>
    </li>
    <li><strong>Azure Resources</strong>
        <ul>
            <li>Disk Encryption</li>
            <li>Storage Account Encryption</li>
        </ul>
    </li>
</ul>
<p>Designed for DevOps teams and cloud security professionals to:</p>
<ul>
    <li>Automate compliance monitoring</li>
    <li>Identify misconfigured resources</li>
    <li>Generate audit-ready reports</li>
    <li>Maintain encryption standards</li>
</ul>

<h2 id="key-features">Key Features</h2>
<ul>
    <li>✅ <strong>Multi-Cloud Support</strong></li>
    <li>✅ <strong>Asynchronous Operations</strong></li>
    <li>✅ <strong>Detailed Compliance Reporting</strong></li>
    <li>✅ <strong>Centralized Configuration</strong></li>
    <li>✅ <strong>Comprehensive Logging</strong></li>
    <li>✅ <strong>Thread Pool Optimization</strong></li>
    <li>✅ <strong>Pagination Support</strong></li>
    <li>✅ <strong>Error Handling</strong></li>
</ul>

<h2 id="use-case-scenarios">Use Case Scenarios</h2>

<h3>1. Daily Compliance Check</h3>
<p><strong>Scenario:</strong> Security team needs daily assurance of encryption status</p>
<p><strong>Solution:</strong></p>
<pre><code># Add to cron job
0 2 * * * /path/to/python /project/src/main.py
</code></pre>

<h3>2. Audit Preparation</h3>
<p><strong>Scenario:</strong> Preparing for PCI-DSS audit requiring encryption documentation</p>
<p><strong>Solution:</strong></p>
<pre><code># Generate timestamped report
python -m src.main
# Output: compliance_report_20230815_143022.json
</code></pre>

<h3>3. Incident Response</h3>
<p><strong>Scenario:</strong> Security breach investigation requires immediate encryption status check</p>
<p><strong>Solution:</strong></p>
<pre><code># Run with debug logging
LOG_LEVEL=DEBUG python -m src.main
</code></pre>

<h3>4. New Resource Onboarding</h3>
<p><strong>Scenario:</strong> Validate encryption for newly created cloud resources</p>
<p><strong>Solution:</strong></p>
<pre><code>from src.aws.compliance import AwsComplianceAuditor

async def validate_new_resources():
    auditor = AwsComplianceAuditor()
    return await auditor.check_encryption()
</code></pre>

<h2 id="installation">Installation</h2>

<h3>Prerequisites</h3>
<ul>
    <li>Python 3.8+</li>
    <li>AWS CLI configured</li>
    <li>Azure CLI authenticated</li>
</ul>

<h3>Setup</h3>
<pre><code># Clone repository
git clone https://github.com/yourrepo/cloud-compliance-audit.git
cd cloud-compliance-audit

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
</code></pre>

<h2 id="configuration">Configuration</h2>
<p>Edit <code>.env</code> file:</p>
<pre><code># AWS Configuration
AWS_REGION=us-east-1

# Azure Configuration
AZURE_SUBSCRIPTION_ID=your-subscription-id

# Application Settings
LOG_LEVEL=INFO
MAX_WORKERS=8
REPORT_DIR=./reports
</code></pre>

<p><strong>Required Permissions:</strong></p>
<ul>
    <li>AWS: <code>AmazonEC2ReadOnlyAccess</code>, <code>AmazonS3ReadOnlyAccess</code></li>
    <li>Azure: <code>Reader</code>, <code>Storage Account Contributor</code></li>
</ul>

<h2 id="usage">Usage</h2>

<h3>Command Line</h3>
<pre><code># Standard audit
python -m src.main

# Custom region (AWS only)
AWS_REGION=eu-west-1 python -m src.main

# Save reports to different location
REPORT_DIR=/mnt/audits python -m src.main
</code></pre>

<h3>Sample Output</h3>
<pre><code>{
  "timestamp": "2023-08-15T14:30:22.123456",
  "aws": {
    "ebs": {"encrypted": 42, "total": 45, "compliance_status": "NON_COMPLIANT"},
    "s3": {"encrypted": 18, "total": 18, "compliance_status": "COMPLIANT"},
    "overall": "NON_COMPLIANT"
  },
  "azure": {
    "disks": {"encrypted": 30, "total": 30, "compliance_status": "COMPLIANT"},
    "storage": {"encrypted": 12, "total": 12, "compliance_status": "COMPLIANT"},
    "overall": "COMPLIANT"
  },
  "overall_status": "NON_COMPLIANT",
  "execution_time": 8.24
}
</code></pre>

<h3>Programmatic Use</h3>
<pre><code>from src.main import generate_report
from src.aws.compliance import AwsComplianceAuditor

async def custom_audit():
    # Run full audit
    full_report = await generate_report()
    
    # AWS-only check
    aws_auditor = AwsComplianceAuditor(region='ap-southeast-2')
    aws_status = await aws_auditor.check_encryption()
    
    return full_report, aws_status
</code></pre>

<h2 id="report-structure">Report Structure</h2>
<table>
    <thead>
        <tr>
            <th>Field</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>timestamp</td>
            <td>ISO 8601 report generation time</td>
        </tr>
        <tr>
            <td>aws</td>
            <td>AWS compliance status</td>
        </tr>
        <tr>
            <td>azure</td>
            <td>Azure compliance status</td>
        </tr>
        <tr>
            <td>overall_status</td>
            <td>Combined compliance status</td>
        </tr>
        <tr>
            <td>execution_time</td>
            <td>Total runtime in seconds</td>
        </tr>
    </tbody>
</table>

<p><strong>Compliance Status Values:</strong></p>
<ul>
    <li><code>COMPLIANT</code>: 100% resources encrypted</li>
    <li><code>NON_COMPLIANT</code>: &lt;100% compliance</li>
    <li><code>ERROR</code>: Check failed</li>
</ul>

<h2 id="extending-the-tool">Extending the Tool</h2>

<h3>Add New Checks</h3>
<ol>
    <li>Create new method in <code>src/aws/compliance.py</code>:
        <pre><code>def _check_rds_encryption(self):
    rds = self.client.rds
    # Implementation here
</code></pre>
    </li>
    <li>Update <code>check_encryption</code> method:
        <pre><code>async def check_encryption(self):
    rds_task = loop.run_in_executor(...)
    results = await asyncio.gather(..., rds_task)
    # Update return dict
</code></pre>
    </li>
</ol>

<h3>Support New Cloud Providers</h3>
<ol>
    <li>Create new directory <code>src/gcp/</code></li>
    <li>Implement client and compliance classes</li>
    <li>Update <code>main.py</code> to include new provider</li>
</ol>

<h2 id="troubleshooting">Troubleshooting</h2>

<h3>Common Issues</h3>
<ol>
    <li><strong>Authentication Errors</strong>
        <ul>
            <li>Verify AWS CLI/Azure CLI login</li>
            <li>Check credential expiration times</li>
        </ul>
    </li>
    <li><strong>Permission Denied</strong>
        <ul>
            <li>Validate IAM roles have required permissions</li>
            <li>Check Azure AD application registration</li>
        </ul>
    </li>
    <li><strong>Missing Dependencies</strong>
        <pre><code>pip install --force-reinstall -r requirements.txt
</code></pre>
    </li>
    <li><strong>Partial Results</strong>
        <pre><code>LOG_LEVEL=DEBUG python -m src.main > debug.log 2>&1
</code></pre>
    </li>
</ol>

<h2 id="contributing">Contributing</h2>
<ol>
    <li>Fork the repository</li>
    <li>Create feature branch</li>
    <li>Add tests for new features</li>
    <li>Submit pull request</li>
</ol>

<p><strong>Testing Guidelines</strong></p>
<pre><code># Run all tests
python -m pytest tests/

# AWS-specific tests
python -m pytest tests/test_aws_compliance.py -v
</code></pre>

<h2 id="license">License</h2>
<p>Apache 2.0 - See <a href="LICENSE">LICENSE</a> for details.</p>

<h2 id="contact">Contact</h2>
<p>For security issues or enterprise support:</p>
<ul>
    <li><a href="mailto:paqads.ca@gmail.com">paqads.ca@gmail.com</a></li>
</ul>

<p>
    <span class="badge badge-orange">Cloud Security</span>
    <span class="badge badge-green">NIST Compliant</span>
</p>

</body>
</html>
