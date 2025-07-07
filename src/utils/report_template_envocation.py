import json
import re
from typing import Dict, Literal, List

from pydantic import BaseModel, Field

from utils.azure_client_utils import get_client_and_deployment_name
from utils.utils import describe_LDAP, describe_report_properties


class StructuredReportDescriptionAnswringFormat(BaseModel):
    filters:        List[str] = Field(description="List of filters applied to the report.")
    display_fields: List[str] = Field(description="List of display fields used in the report.")


class LDAPQueryAnsweringFormat(BaseModel):
    confidence: Literal["yes", "maybe", "no"] = Field(description="The confidence level that this report can be mimicked by an LDAP query.")
    reasoning:  str                           = Field(description="The reasoning behind the conclusion, explaining why it is likely an LDAP report.")
    ldap_query: str                           = Field(description="An LDAP query that mimics the report in the best way possible.")



def generate_structured_xml_description_request_prompt(xml_report_str) -> str:
    """
    Generates a prompt for the model to describe the structure of an XML report.
    The model should return a structured description of the report, including filters and display fields.
    """
    response_format = '{"filters": List[str], "display_fields": List[str]}'

    res = f"""Here is an XML report format:
<report>
{xml_report_str}
</report>
Please describe the structure of the report in a structured way: I want to get the Active Directory / Event log filters applied and the display fields used in this report.
Response format:{response_format}"""
    return res



def generate_structured_xml_report_description(
    client, deployment_name: str,
    xml_report_str: str
) -> str:
    # Get the structured reply using the tool
    completion = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {"role": "system", "content": "You're a helpful assistant that breaks down reports to their components."},
            {"role": "user", "content": generate_structured_xml_description_request_prompt(xml_report_str)},
        ],
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "get_answering_schema",
                    "description": "Get the schema for the desired response based on user input.",
                    "parameters": StructuredReportDescriptionAnswringFormat.model_json_schema(),
                },
            }
        ],
        tool_choice={
            "type": "function",
            "function": {"name": "get_answering_schema"},
        },
    )

    tool_call = completion.choices[0].message.tool_calls[0]
    json_arguments = tool_call.function.arguments

    # Parse and pretty-print the JSON
    parsed_json = json.loads(json_arguments)
    structured_xml_description = '\n'.join([
        "Here is a structured description of the XML report:",
        "Filters applied: ",
        ', '.join(parsed_json["filters"]),
        "Display fields used: ",
        ', '.join(parsed_json["display_fields"])
    ])
    return structured_xml_description


def generate_ldap_request_prompt(
    xml_report_str: str,
    report_structured_description: str  # This is a structured description of the original XML report, including filters and display fields
) -> str:
    response_format = """{"confidence": "yes" / "maybe" / "no",
"reasoning": "explain why you think this is an LDAP report or not",
"ldap_query": Either way, do your best to generate an LDAP query that mimics this report in the best way you can.}"""
    
    
    return f"""Here is an XML report format:
<report>
{xml_report_str}
</report>

For your convenience, here is a structured description of the report:
{report_structured_description}

How confident are you that a similar report could, in principle, be generated from an LDAP query?

Note: An LDAP query is a query that can be run against an Active Directory server to retrieve information about objects in the directory, such as users, computers, and groups.
Example 1: (&(objectCategory=person)(memberOf=CN=HR,OU=Groups,DC=example,DC=com)(mail=*))
Example 2: (|(objectClass=user)(objectClass=contact))
Example 3: (&
  (objectCategory=person)
  (objectClass=user)
  (!(userAccountControl:1.2.840.113556.1.4.803:=2))
  (memberOf=CN=Sales,OU=Groups,DC=example,DC=com)
  (displayName=A*)
  (mail=*)
)
Example 4: (&
  (objectClass=group)
  (cn=*VPN*)
)

return your answer in this format:
{response_format}
"""

def generate_ldap_query(
    client, deployment_name: str,
    xml_report_str: str, # This is the XML report string
    report_structured_description: str # This is a structured description of the original XML report, including filters and display fields
    ) -> str:
    """
    Generates an LDAP query based on the quest report string and report type.
    This is a placeholder function and should be implemented with actual logic.
    """    
    # Get the structured reply using the tool
    completion = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {"role": "system", "content": "You're a helpful assistant that generates LDAP queries."},
            {"role": "user", "content": generate_ldap_request_prompt(xml_report_str, report_structured_description)},
        ],
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "get_answering_schema",
                    "description": "Get the schema for the desired response based on user input.",
                    "parameters": LDAPQueryAnsweringFormat.model_json_schema(),
                },
            }
        ],
        tool_choice={
            "type": "function",
            "function": {"name": "get_answering_schema"},
        },
    )

    tool_call = completion.choices[0].message.tool_calls[0]
    json_arguments = tool_call.function.arguments

    # Parse and pretty-print the JSON
    parsed_json = json.loads(json_arguments)
    confidence = parsed_json["confidence"]
    reasoning = parsed_json["reasoning"]
    
    # print(f"Confidence: {confidence}"
    #       f"\nReasoning: {reasoning}")
    
    ldap_query = parsed_json["ldap_query"]
    return ldap_query



def generate_ldap_report(
    client, deployment_name: str,
    quest_report_str: str,
    report_type: Literal["LDAP", "DNS", "NonDNS"],
    report_structured_description: str, # This is a structured description of the original XML report, including filters and display fields
    desired_report_description: str,
    temperature: float,
) -> str:
    ldap_query = generate_ldap_query(client, deployment_name, quest_report_str, report_structured_description)
    
    report_content = get_ldap_content(ldap_query, )
    meta           = get_ldap_meta(ldap_query, report_content)
    result = {
        "content": report_content,
        "meta": meta,
        "SecurityReportSettings": None,
        "CustomLogic": None
    }
    return result


def generate_dns_report(
    client, deployment_name: str,
    quest_report_str: str,
    report_type: Literal["LDAP", "DNS", "NonDNS"],
    report_structured_description: str, # This is a structured description of the original XML report, including filters and display fields
    desired_report_description: str,
    temperature: float,
) -> str:
    # TODO
    return None


def generate_nondns_report(
    client, deployment_name: str,
    quest_report_str: str,
    report_type: Literal["LDAP", "DNS", "NonDNS"],
    report_structured_description: str, # This is a structured description of the original XML report, including filters and display fields
    desired_report_description: str,
    temperature: float,
) -> str:
    # TODO
    return None


def describe_desired_report_properties(report_type: str) -> str:
    if report_type in ["DNS", "NonDNS"]:
        return describe_report_properties(
            report_type=report_type, filters_or_displays="both"
        )
    return describe_LDAP()


def get_reports(
    client, deployment_name: str,
    report_type: Literal["LDAP", "DNS", "NonDNS"],
    likelihood: Literal["yes", "maybe", "no"],
    xml_report_str: str,  # This is the XML report string
) -> list:
    
    temperatures = {
        "yes": [0, 0.2],
        "maybe": [0.0],
        "no": [],
    }[likelihood]

    func = {
        "LDAP": generate_ldap_report,
        "DNS": generate_dns_report,
        "NonDNS": generate_nondns_report,
    }[report_type]

    # post_process = {
    #     "LDAP": post_process_ldap_report,
    #     "DNS": post_process_dns_report,
    #     "NonDNS": post_process_nondns_report,
    # }[report_type]

    desired_report_description = describe_desired_report_properties(report_type)
    original_report_description = generate_structured_xml_report_description(client, deployment_name, xml_report_str)

    results = []

    for temperature in temperatures:
        report = func(
            client, deployment_name,
            xml_report_str, # This is the XML report string
            report_type,
            original_report_description, # This is a structured description of the original XML report, including filters and display fields
            desired_report_description,
            temperature,
        )
        # post_processed = post_process(report, report_type)
        # results.append(post_processed)

    return results

def structurly_describe_report(quest_report_str: str) -> str:
    response_fomat = """{"filters_applied": List[str] list of filters applied to the report, "display_fields_used": List[str] list of display fields used in the report}"""
    prompt = f"""Here is a Quest report in XML format:
<report>
{quest_report_str}
</report>
Please describe the structure of the report in a structured way, including the filters applied and the display fields used.
Return your answer in this format:
{response_fomat}"""

    

def generate_reports_from_likely_report_types(
    report_type_to_likelihood: dict,
    quest_report_str: str,
):
    client, deployment_name = get_client_and_deployment_name()
    generated_report = {}
    for report_type in report_type_to_likelihood:
        generated_report[report_type] = get_reports(
            client, deployment_name,
            report_type,
            report_type_to_likelihood[report_type],
            quest_report_str,
            
        )
    return generated_report
