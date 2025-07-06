import json
from typing import Any, Dict, List, Tuple


def get_breakdown(
    client, model_name, query: str, tools: List[Dict[str, Any]]
) -> Dict[str, Any]:
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
        model=model_name,
        messages=messages,
        tools=tools,
        tool_choice={
            "type": "function",
            "function": {"name": "get_breakdown_schema"},
        },
    )

    tool_call = completion.choices[0].message.tool_calls[0]
    json_arguments = tool_call.function.arguments

    parsed_json = json.loads(json_arguments)

    return parsed_json  # Return parsed JSON


def infer_db_report_type(
    DNS_filters: bool,
    DNS_displays: bool,
    NonDNS_filters: bool,
    NonDNS_displays: bool,
) -> Tuple[bool, str]:
    something_about_dns = any([DNS_filters, DNS_displays])
    something_about_nondns = any([NonDNS_filters, NonDNS_displays])

    if something_about_dns and not something_about_nondns:
        return True, "DB_DNS"

    if something_about_nondns and not something_about_dns:
        return True, "DB_NonDNS"

    if something_about_dns and something_about_nondns:
        return (
            False,
            """The user input contains both DNS and Non-DNS database-related queries, which is ambiguous. "
            "Please clarify whether the report should focus on DNS or Non-DNS details.""",
        )

    return (
        False,
        """The user input does not provide enough information to determine the DB report type.""",
    )


def infer_report_type_from_user_input(
    current_status: bool,
    historical_changes: bool,
    DNS_filters: bool,
    DNS_displays: bool,
    NonDNS_filters: bool,
    NonDNS_displays: bool,
) -> Tuple[bool, str]:
    if current_status and not historical_changes:
        return True, "LDAP"

    if not current_status and historical_changes:
        return infer_db_report_type(
            DNS_filters=DNS_filters,
            DNS_displays=DNS_displays,
            NonDNS_filters=NonDNS_filters,
            NonDNS_displays=NonDNS_displays,
        )

    if current_status and historical_changes:
        return (
            False,
            "The user input contains both current status and database-related queries, which is ambiguous. Please clarify whether the report should focus on LDAP or database details.",
        )

    return (
        False,
        "The user input does not provide enough information to determine the report type.",
    )
