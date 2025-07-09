import json
import re
from typing import Any, Dict, Literal

from pydantic import BaseModel, Field

from src.reports_generators.DNS import dns_post_process, get_dns_content, get_dns_meta
from src.reports_generators.NonDNS import get_nondns_content, get_nondns_meta, nondns_post_process
from src.reports_generators.LDAP import get_ldap_content, get_ldap_meta, ldap_post_process
from src.utils.azure_client_utils import ask_with_schema, get_client_and_deployment_name
from src.utils.utils import describe_LDAP, describe_report_properties


class LDAPQueryAnsweringFormat(BaseModel):
    confidence: Literal["yes", "maybe", "no"] = Field(description="The confidence level that this report can be mimicked by an LDAP query.")
    reasoning:  str = Field(description="The reasoning behind the conclusion, explaining why it is likely an LDAP report.")
    ldap_query: str = Field(description="An LDAP query that mimics the report in the best way possible.")


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


def generate_ldap_request_prompt(
    xml_report_str: str,
    report_description: str  # This is a structured description of the original XML report, including filters and display fields
) -> str:
    response_format = """{"confidence": "yes" / "maybe" / "no",
"reasoning": "explain why you think this is an LDAP report or not",
"ldap_query": Either way, do your best to generate an LDAP query that mimics this report in the best way you can.}"""
    
    
    return f"""Here is an XML report format:
<report>
{xml_report_str}
</report>

For your convenience, here is also a description of the report:
{report_description}

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
    # client, deployment_name: str,
    xml_report_str: str, # This is the XML report string
    original_quest_report_description: str # This is a structured description of the original XML report, including filters and display fields
    ) -> str:
    system_prompt = "You're a helpful assistant that generates LDAP queries."
    prompt = generate_ldap_request_prompt(xml_report_str, original_quest_report_description)
    parsed_json = ask_with_schema(system_prompt=system_prompt, prompt=prompt, schema=LDAPQueryAnsweringFormat)
    
    # print(f"Confidence: {parsed_json['confidence']}"
    #       f"\nReasoning: {parsed_json['reasoning']}")
    
    ldap_query = parsed_json["ldap_query"]
    return ldap_query



def generate_ldap_report(
    quest_report_str: str,
    report_description: str, # This is the free text extracted from the report
    desired_report_description: str, # This is a description of the desired report, including filters and display fields
    temperature: float,
) -> str:
    ldap_query = generate_ldap_query(xml_report_str=quest_report_str,
                                     original_quest_report_description=report_description)
    report_content = get_ldap_content(quest_report_str=quest_report_str,
                                      report_description=report_description,
                                      ldap_query=ldap_query,
                                      description_of_an_ldap_report=desired_report_description,
                                      temperature=temperature)
    metadata = get_ldap_meta(quest_report_str=quest_report_str,
                                   report_description=report_description,
                                   ldap_query=ldap_query,
                                   temperature=temperature,
                                   the_content_field_of_the_ldap_report=report_content)
    result = {"Content": report_content,
              "MetaData": metadata,
              "SecurityReportSettings": None,
              "CustomLogic": None}
    return result


def generate_dns_report(
    quest_report_str: str,
    report_description: str, # This is the free text extracted from the report
    desired_report_description: str, # This is a description of the desired report, including filters and display fields
    temperature: float,
) -> str:
    report_content = get_dns_content(quest_report_str,
                                     report_description,
                                     desired_report_description,
                                     temperature)
    metadata = get_dns_meta(quest_report_str,
                            report_description,
                            temperature,
                            report_content)
    result = {"Content": report_content,
              "MetaData": metadata,
              "SecurityReportSettings": None,
              "CustomLogic": None}
    return result


def generate_nondns_report(
    quest_report_str: str,
    report_description: str, # This is the free text extracted from the report
    desired_report_description: str, # This is a description of the desired report, including filters and display fields
    temperature: float,
) -> str:
    report_content = get_nondns_content(quest_report_str,
                                        report_description,
                                        desired_report_description,
                                        temperature)
    metadata = get_nondns_meta(quest_report_str,
                                     report_description,
                                     temperature,
                                     report_content)
    result = {"Content": report_content,
              "MetaData": metadata,
              "SecurityReportSettings": None,
              "CustomLogic": None}
    return result


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
    extracted_data: str,  # This is a free text extracted from the report
) -> list:
    
    temperatures = {
        "yes": [0, 0.2, 0.4],
        "maybe": [0.1, 0.3],
        "no": [],
    }[likelihood]

    desired_report_description = describe_desired_report_properties(report_type)

    results = []

    for temperature in temperatures:
        if report_type == "LDAP":
            report = generate_ldap_report(
                xml_report_str, # This is the XML report string
                extracted_data, # This is a free text extracted from the report
                desired_report_description,
                temperature)
            post_processed = ldap_post_process(report)
        elif report_type == "DNS":
            report = generate_dns_report(
                xml_report_str, # This is the XML report string
                extracted_data, # This is a free text extracted from the report
                desired_report_description,
                temperature)
            post_processed = dns_post_process(report)
        else:
            # meaning report_type == "NonDNS":
            report = generate_nondns_report(
                xml_report_str, # This is the XML report string
                extracted_data, # This is a free text extracted from the report
                desired_report_description,
                temperature)
            post_processed = nondns_post_process(report)
        
        results.append(post_processed)

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
    extracted_data: str
):
    """Generates reports based on the likely report types and the quest report string.
    Args:
        report_type_to_likelihood (dict): A dictionary mapping report types to their likelihoods.
        quest_report_str (str): The string representation of the quest report.
        extracted_data (str): Additional data extracted from the report as free text.
    """
    client, deployment_name = get_client_and_deployment_name()
    generated_report: Dict[str, Dict[int, Any]] = {}
    for report_type in report_type_to_likelihood:
        generated_report[report_type] = get_reports(
            client=client,
            deployment_name=deployment_name,
            report_type=report_type,
            likelihood=report_type_to_likelihood[report_type],
            xml_report_str=quest_report_str,
            extracted_data=extracted_data
            
        )
    return generated_report
