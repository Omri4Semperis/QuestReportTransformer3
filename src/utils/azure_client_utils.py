import json
from typing import Optional
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

def ask(system_prompt: Optional[str], prompt: str, temperature: float = 0.25) -> str:
    system_prompt = system_prompt or "You are a helpful assistant. Reply briefly."
    
    client, deployment_name = get_client_and_deployment_name()
    
    print(f"\n\n=====\n\nASKING {deployment_name} (t={temperature}):\n{system_prompt[:100]}...\n\n{prompt[:100]}...\n---------\n")
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]

    response = client.chat.completions.create(
        model=deployment_name,
        messages=messages,
        temperature=temperature,
    )
    result = response.choices[0].message.content
    
    print(f"Response from {deployment_name}:\n{result[:100]}...\n---------\n")
    
    return result

def ask_with_schema(system_prompt: Optional[str], prompt: str, schema, temperature: float = 0.25):
    system_prompt = system_prompt or "You are a helpful assistant. Reply briefly according to the schema."
    
    client, deployment_name = get_client_and_deployment_name()
    
    print(f"\n\n=====\n\nASKING {deployment_name} (t={temperature}) with schema {schema.__name__}:\n{system_prompt[:100]}...\n\n{prompt[:100]}...\n---------\n")
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]

    response = client.chat.completions.create(
        model=deployment_name,
        messages=messages,
        tools=[
            {
                "type": "function",
                "function": {
                    "name": schema.__name__,
                    "description": "Get the structured response based on the provided schema.",
                    "parameters": schema.model_json_schema(),
                },
            }
        ],
        tool_choice={
            "type": "function",
            "function": {"name": schema.__name__},
        },
        temperature=temperature,
    )

    tool_call = response.choices[0].message.tool_calls[0]
    json_arguments = tool_call.function.arguments

    # Parse and pretty-print the JSON
    parsed_json = json.loads(json_arguments)

    print(f"Response from {deployment_name} with schema {schema.__name__}:\n{str(json.dumps(parsed_json, indent=2)[:100])}...\n---------\n")
    
    return parsed_json