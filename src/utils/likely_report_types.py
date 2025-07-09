import json
from typing import Dict, Literal, List, Any
from pydantic import BaseModel, Field

from src.utils.azure_client_utils import ask_with_schema, get_client_and_deployment_name
from src.utils.utils import describe_LDAP, describe_report_properties


class LDAPLikelihoodSchema(BaseModel):
    """How likely is it that a user's description of a report is about an LDAP report."""

    conclusion: Literal["yes", "no", "maybe"] = Field(
        description="The conclusion about whether the report is an LDAP report."
    )
    reasoning: str = Field(
        description="The reasoning behind the conclusion, explaining why it is likely an LDAP report."
    )


class DNSLikelihoodSchema(BaseModel):
    """How likely is it that a user's description of a report is about a DNS report."""

    conclusion: Literal["yes", "no", "maybe"] = Field(
        description="The conclusion about whether the report is a DNS report."
    )
    reasoning: str = Field(
        description="The reasoning behind the conclusion, explaining why it is likely a DNS report."
    )


class NonDNSLikelihoodSchema(BaseModel):
    """How likely is it that a user's description of a report is about a NonDNS report."""

    conclusion: Literal["yes", "no", "maybe"] = Field(
        description="The conclusion about whether the report is a NonDNS report."
    )
    reasoning: str = Field(
        description="The reasoning behind the conclusion, explaining why it is likely a NonDNS report."
    )


class ReportTypeHints(BaseModel):
    """
    Schema for the report type hints based on user input.
    This schema is used to infer the type of report based on the user's description.
    """

    LDAP: LDAPLikelihoodSchema = Field(
        description="Likelihood and reasoning why this report might be an LDAP report."
    )
    DNS: DNSLikelihoodSchema = Field(
        description="Likelihood and reasoning why this report might be a DNS report."
    )
    NonDNS: NonDNSLikelihoodSchema = Field(
        description="Likelihood and reasoning why this report might be a NonDNS report."
    )


def get_prompt_about_likely_report_types(quest_report_str, extracted_data) -> str:
    """
    Returns the system message prompt for determining likely report types.
    """
    result_example = str(
        {
            "LDAP": {
                "conclusion": "maybe",
                "reasoning": "There are mostly requests about current situation",
            },
            "DNS": {
                "conclusion": "no",
                "reasoning": "I see no filters nor display fields of the DNS report",
            },
            "NonDNS": {
                "conclusion": "yes",
                "reasoning": "There are requests about historical changes and filters that are typical for NonDNS reports",
            },
        }
    )

    prompt = f"""
I can produce 3 kinds of reports: LDAP, DNS and NonDNS. Here is some information about the 3 kinds:

# LDAP:
{describe_LDAP()}

# DNS and NonDNS:
{describe_report_properties(report_type="both", filters_or_displays="both")}

For each of these 3 kinds (LDAP, DNS, NonDNS), I'd like you look at the following XML report template- and tell me how likely it is to be of that kind.
For example, if it might be LDAP, definitely not DNS and very likely NonDNS, then return: {result_example}.

Here's the report template:
<The XML file starts here>
{quest_report_str}
<The XML file ends here>

Here's some extracted information about the report:
{extracted_data}

Here's your working process:
1. Read the report template.
2. Analyze the content of the report template.
3. Determine if the report is likely to be LDAP, DNS, or NonDNS based on the content.
4. Return a dictionary with keys "LDAP", "DNS", and "NonDNS" and values "yes", "no", or "maybe" based on your analysis.
5. You may add comments to your response in the designated fields.
"""
    return prompt


def complete_likelihoods(
    system_message, prompt, answer_format
):
    # mocked_response = {
    #     "LDAP": {
    #         "conclusion": "maybe",
    #         "reasoning": "There are mostly requests about current situation",
    #     },
    #     "DNS": {
    #         "conclusion": "no",
    #         "reasoning": "There are no DNS-related queries",
    #     },
    #     "NonDNS": {
    #         "conclusion": "yes",
    #         "reasoning": "There are several non-DNS related requests",
    #     },
    # }
    # print(
    #     "===============\nWARNING: Using mocked response for testing purposes.\n==============="
    # )
    # return mocked_response

    parsed_json = ask_with_schema(system_prompt=system_message,
                                  prompt=prompt,
                                  schema=answer_format)
    return parsed_json
    # client, deployment_name = get_client_and_deployment_name()

    # # Get the structured reply using the tool
    # completion = client.chat.completions.create(
    #     model=deployment_name,
    #     messages=[
    #         {"role": "system", "content": system_message},
    #         {"role": "user", "content": prompt},
    #     ],
    #     tools=[
    #         {
    #             "type": "function",
    #             "function": {
    #                 "name": "get_answering_schema",
    #                 "description": "Get the schema for the desired response based on user input.",
    #                 "parameters": answer_format.model_json_schema(),
    #             },
    #         }
    #     ],
    #     tool_choice={
    #         "type": "function",
    #         "function": {"name": "get_answering_schema"},
    #     },
    # )

    # tool_call = completion.choices[0].message.tool_calls[0]
    # json_arguments = tool_call.function.arguments

    # # Parse and pretty-print the JSON
    # parsed_json = json.loads(json_arguments)
    # return parsed_json


def ask_user_for_type_confirmation(assumed_type: str, likelihood: str, reasoning: str):
    likelihood_phrasing = {
        "yes": "is probably (=2)",
        "no": "is probably NOT (=0)",
        "maybe": "might be (=1)",
    }[likelihood]
    
    print(f"""Since {reasoning},
This report {likelihood_phrasing} of type: {assumed_type.upper()}.
Do you agree with this conclusion? Enter 0=no, 1=maybe, or 2=yes, empty response=agree with whatever I decided.""")
    
    user_input = input()

    the_user_thinks = {"0": "no", "1": "maybe", "2": "yes", "": likelihood}

    if user_input not in the_user_thinks:
        print("Invalid input. Assuming agreement with the decision.")
        return likelihood
    
    return the_user_thinks[user_input]


def confirm_with_user(parsed_completion: Dict[str, Any]) -> Dict[str, Any]:
    """
    Confirm the parsed completion with the user.
    This function can be extended to include user interaction for confirmation.
    For now, it simply returns the parsed completion.
    """
    # Here you can implement a confirmation step with the user if needed
    # For example, you could print the result and ask for confirmation
    result = {}
    for key, value in parsed_completion.items():
        likelihood = value["conclusion"]
        reasoning = value["reasoning"]
        user_wants = ask_user_for_type_confirmation(key, likelihood, reasoning)

        result[key] = user_wants
    return result


def get_likely_report_types(
    quest_report_str: str, extracted_data: str
) -> Dict[Literal["LDAP", "DNS", "NonDNS"], Literal["yes", "no", "maybe"]]:
    """
    Analyzes the quest report string and determines the likely report types.
    Args:
        quest_report_str (str): The string representation of the quest report.
        extracted_data (str): Additional data extracted from the report as free text.
    """
    # Analyze the quest_report_str and determine the likely report types
    # For now, we'll return a dummy implementation
    system_message = "You are a helpful assistant that analyzes reports and determines what kinds of report they could be. You pay attention to functionality, fields names etc."
    prompt = get_prompt_about_likely_report_types(quest_report_str, extracted_data)
    parsed_completion = complete_likelihoods(system_message, prompt, answer_format=ReportTypeHints)
    the_user_confirmed_likelihood = confirm_with_user(parsed_completion)
    return the_user_confirmed_likelihood
