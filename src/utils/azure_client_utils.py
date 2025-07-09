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

def trim_to_len(s: str, length: int = 120) -> str:
    """
    Trims the string to a specified length, adding an ellipsis if it exceeds that length.
    """
    for i in range(20, 1, -1):
        s = s.replace(" " * i, " ")
        s = s.replace("\t" * i, " ")
        s = s.replace("\n" * i, " ")
    s = s.replace('\u200b', '')  # Remove zero-width spaces
    s = s.strip().replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
    
    if len(s) > length:
        return s[:length] + "..."
    return s

def announce_llm_interaction(deployment_name: str, system_prompt: str, prompt: str, temperature: float = 0.25, schema: Optional[str] = None) -> None:
    print('\n' + '=' * 20)
    print(f"Calling {deployment_name} (t={temperature})")
    if schema:
        print(f"[Schema:  \t{schema.__name__}]")
    print(f"System: \t{trim_to_len(system_prompt)}")
    print(f"Prompt: \t{trim_to_len(prompt)}")
    print('-' * 20)
    print("Waiting...", end='\r')

def announce_reply(reply_as_plain_text: str) -> None:
    print(f"Reply:  \t{trim_to_len(reply_as_plain_text)}")
    print('=' * 20)

def ask(system_prompt: Optional[str], prompt: str, temperature: float = 0.25) -> str:
    system_prompt = system_prompt or "You are a helpful assistant. Reply briefly."
    
    client, deployment_name = get_client_and_deployment_name()
    
    announce_llm_interaction(deployment_name, system_prompt, prompt, temperature)
    
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

    announce_reply(result)

    return result

def ask_with_schema(system_prompt: Optional[str], prompt: str, schema, temperature: float = 0.25):
    system_prompt = system_prompt or "You are a helpful assistant. Reply briefly according to the schema."
    
    client, deployment_name = get_client_and_deployment_name()
    
    announce_llm_interaction(deployment_name, system_prompt, prompt, temperature, schema)
    
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

    reply_as_plain_text = str(json.dumps(parsed_json, indent=2))
    announce_reply(reply_as_plain_text)
    
    return parsed_json