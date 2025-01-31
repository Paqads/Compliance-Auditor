import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
    AZURE_SUBSCRIPTION_ID = os.getenv('AZURE_SUBSCRIPTION_ID')
    
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    MAX_WORKERS = int(os.getenv('MAX_WORKERS', 10))

settings = Settings()