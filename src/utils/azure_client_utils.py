from dotenv import load_dotenv
from openai import AzureOpenAI
import os


def get_client_and_deployment_name():
    load_dotenv()

    api_key = os.getenv("AZURE_API_KEY")
    api_version = os.getenv("AZURE_API_VERSION")
    azure_endpoint = os.getenv("AZURE_API_BASE")
    deployment_name = "gpt-4o"  # As specified in the original script

    # Initialize the Azure OpenAI client
    client = AzureOpenAI(
        api_key=api_key.strip(),
        api_version=api_version.strip(),
        azure_endpoint=azure_endpoint.strip(),
        timeout=30.0,
    )

    return client, deployment_name
