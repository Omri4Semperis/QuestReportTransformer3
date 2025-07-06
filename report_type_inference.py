from decision_making import AmbiguousReportTypeError, infer_report_type_from_user_input
from src.schemas.meta.report_type_hints import ReportTypeHints

import json
from typing import Dict, List, Any
import os

from dotenv import load_dotenv
from openai import (
    AzureOpenAI,
)

print("Azure OpenAI client initialized successfully.")


def get_breakdown(client, query: str, tools: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Ask for a report and return the structured hints.
    :param quesry: The user query for the report.
    :return: Parsed JSON with report type hints.
    """

    messages = [
        {"role": "system", "content": "You are a helpful assistant. Reply briefly."},
        {"role": "user", "content": query},
    ]

    completion = client.chat.completions.create(
        model=deployment_name,
        messages=messages,
        tools=tools,
        tool_choice={
            "type": "function",
            "function": {"name": "get_ReportTypeHintsSchema"},
        },
    )

    tool_call = completion.choices[0].message.tool_calls[0]
    json_arguments = tool_call.function.arguments

    parsed_json = json.loads(json_arguments)

    return parsed_json  # Return parsed JSON


def manage_inference(client, query, tools):
    """
    Manages the inference process for report type based on user query.
    """
    success = False
    max_attempts = 3

    for attempt in range(max_attempts):
        print(f"Attempt {attempt + 1} / {max_attempts}:")
        breakdown = get_breakdown(client, query, tools)

        try:
            report_type = infer_report_type_from_user_input(
                current_status=breakdown.get("asked_for_current_status", False),
                historical_changes=breakdown.get("asked_for_historical_changes", False),
                DNS_filters=breakdown.get("asked_for_DNS_filters", False),
                DNS_displays=breakdown.get("asked_for_DNS_displays", False),
                NonDNS_filters=breakdown.get("asked_for_NonDNS_filters", False),
                NonDNS_displays=breakdown.get("asked_for_NonDNS_displays", False),
            )

        except AmbiguousReportTypeError as e:
            # print(f"Ambiguous report type error: {e}")
            query = (
                query
                + "\nTo be clear, I mean: "
                + input("The report type is ambiguous. Please clarify your request: ")
            )
            continue

        return report_type
    raise AmbiguousReportTypeError(
        "User input does not provide enough information to determine the report type."
    )


if __name__ == "__main__":
    print("Getting everything ready...")

    # Load environment variables from .env file
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

    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_ReportTypeHintsSchema",
                "description": "Get the ReportTypeHints schema based on user input.",
                "parameters": ReportTypeHints.model_json_schema(),
            },
        }
    ]

    for query in [
        # "Create a report about all the users named 'John', who changed their passwords in the last 30 days.",  # nondns,
        # "Create a report about 2024 specific Records type 'SOA'",  # dns
        "Create a report about all the users in the users group 'Marketing'.",  # ldap
    ]:
        print(f"\n\n=====\n\nRequest: {query}\n")
        try:
            infered_type = manage_inference(client, query, tools)
            print(f"Inferred Report Type: {infered_type}\n")
        except AmbiguousReportTypeError as e:
            print(f"This query wasn't clear enough: {e}.\nSkipping this query.\n")
