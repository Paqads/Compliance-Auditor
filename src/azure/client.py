from azure.identity import DefaultAzureCredential
from config.settings import settings

class AzureClient:
    def __init__(self):
        self.credential = DefaultAzureCredential()
        self.subscription_id = settings.AZURE_SUBSCRIPTION_ID

azure_client = AzureClient()