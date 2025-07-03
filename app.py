from src.schemas.Content.PreviewValues.LDAPPreviewValues_schema import LDAPPreviewValuesSchema

import os
import json
from typing import Dict, List, Any

from dotenv import load_dotenv
from openai import AzureOpenAI, RateLimitError, AuthenticationError, APIError, NotFoundError

print("Getting everything ready...")

# Load environment variables from .env file
load_dotenv()

api_key = os.getenv("AZURE_API_KEY")
api_version = os.getenv("AZURE_API_VERSION")
azure_endpoint = os.getenv("AZURE_API_BASE")
deployment_name = "gpt-4o" # As specified in the original script

# Initialize the Azure OpenAI client
client = AzureOpenAI(
    api_key=api_key.strip(),
    api_version=api_version.strip(),
    azure_endpoint=azure_endpoint.strip(),
    timeout=30.0,
)

print("Azure OpenAI client initialized successfully.")

print("""You may ask for an LDAP Preview Values schema response.
Just specify which BaseDNs you're interested in,
What is the Search Scope (Base, One Level, or Sub Tree),
whether global catalog should be enabled or not,
And which value to apply to each field in the LDAP query.
""")

user_input = input("Please enter your request (Enter for default): ")
if not user_input.strip():
    user_input = """I want an LDAP Preview Values schema.
BaseDNs are C=example,DC=com;DC=hello and 'OU=Blah'.
Search in a Sub Tree, with Global Catalog.
objectClass should be sitesContainer, and objectCategory should be 'blah'."""

messages: List[Dict[str, Any]] = [
    {"role": "system", "content": "You are a helpful assistant. Reply briefly."},
    {"role": "user", "content": user_input},
]

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_LDAPPreviewValuesSchema",
            "description": "Get the LDAP Preview Values schema based on user input.",
            "parameters": LDAPPreviewValuesSchema.model_json_schema()
        }
    }
]

# Get the structured reply using the tool
completion = client.chat.completions.create(
    model=deployment_name,
    messages=messages,
    tools=tools,
    tool_choice={
        "type": "function",
        "function": {
            "name": "get_LDAPPreviewValuesSchema"
        }
    }
)

tool_call = completion.choices[0].message.tool_calls[0]
json_arguments = tool_call.function.arguments

print("\nRaw JSON arguments from the model:")
print(json_arguments)

# Parse and pretty-print the JSON
parsed_json = json.loads(json_arguments)
print("\nPretty-printed JSON:")
print(json.dumps(parsed_json, indent=2))