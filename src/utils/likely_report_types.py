import json
from typing import Dict, Literal, List, Any
from pydantic import BaseModel, Field

from utils.azure_client_utils import get_client_and_deployment_name


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


def get_prompt_about_likely_report_types(quest_report_str) -> str:
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
An LDAP report is about Active Directory state, such as user accounts, groups, and organizational units.
It can only be about the current state of Active Directory, not historical changes.
It is typically used to query information that can be retrieved using LDAP queries.
For example, it can be used to find all users in a specific group or to retrieve the attributes of a specific user.

LDAP queries can be short or long. Here are a few examples of LDAP queries:
Find all objects with objectClass = user: (&(objectClass=user))
Find user objects whose login name is jdoe: (&(objectClass=user)(sAMAccountName=jdoe))
Return all group objects: (objectClass=group)
Return users where the disabled flag is NOT set: (&(objectClass=user)(!(userAccountControl:1.2.840.113556.1.4.803:=2)))
Return users who belong to the Admins group: (&(objectClass=user)(memberOf=CN=Admins,CN=Users,DC=example,DC=com))

# DNS and NonDNS:
DNS and NonDNS reports, also called DB Reports, are about historical events or changes that have already occured.
These are not about the current state of Active Directory, but rather about historical data.
DNS reports are specifically about DNS records and their changes, while NonDNS reports can cover a wide range of other historical data.

Both DNS and NonDNS reports can be characterized by the filters they apply and the displays they use.
These filters and displays can be used to narrow down the data that is being queried or displayed.

Here is some parameters that DNS and NonDNS reports share:

## Filters available for both DNS and NonDNS reports
1. Type: Determines if the report is DNS or NonDNS. Mandatory for both DNS and NonDNS. Allowed states: Only state is 'Is'. The input Can only be 'Preset'. Allowed values: DNS or NonDNS.
2. DateRange: The date range to consider. Not mandatory. Allowed states: Only state is 'Is'. The input Can be 'Preset' or 'UserInput'. Allowed values: Can be relative or absolute.
3. Operations: The types of AD operations. Not mandatory. Allowed states: Can only be set to one of these: [Include, Exclude]. The input Can be 'Preset' or 'UserInput'. Allowed values: Multiple choice from: Create, Modify, Add, Remove, Move, Delete, Restore
4. OldValue: The old value of the object's attirubute. Not mandatory. Allowed states: Can only be set to one of these: [Contains, NotContain, Equals, NotEquals IsNotNullAndNotEmpty, IsNullOrEmpty]. The input Can be 'Preset' or 'UserInput'. Allowed values: Free text.
5. NewValue: The new value of the object's attirubute. Not mandatory. Allowed states: Can only be set to one of these: [Contains, NotContain, Equals, NotEquals IsNotNullAndNotEmpty, IsNullOrEmpty]. The input Can be 'Preset' or 'UserInput'. Allowed values: Free text.
6. ChangedBy: The value of the object that caused the change. Not mandatory. Allowed states: Can only be set to one of these: [Contains, NotContain, Equals, NotEquals IsNotNullAndNotEmpty, IsNullOrEmpty]. The input Can be 'Preset' or 'UserInput'. Allowed values: Free text.
7. SourceServers: Domain controllers or DNS servers that are the source of the data Not mandatory. Allowed states: Can only be set to one of these: [Include, Exclude]. The input Can be 'Preset' or 'UserInput'. Allowed values: Closed list: The available Source Servers.
8. ObjectListIds: internal identifiers or unique IDs. Not mandatory. Allowed states: Can only be set to one of these: [Equals, not equals, starts with, ends with]. The input Can be 'Preset' or 'UserInput'. Allowed values: Free text.

## Display fields available for both DNS and NonDNS reports
Category 1: Object & Identity
1. ClassName: Object class (e.g., user, group, computer).
2. DisplayName: User-friendly display name.
3. Distinguished Name: Full LDAP path identifying the object.
4. Object Guid: Unique GUID of the object.
5. SamAccountName: Pre-Windows 2000 logon name.
6. UPN: User Principal Name (user@domain).
7. Version: Version of the record.
Category 2: Report & Collection Metadata
8. CollectionTime: When the data was collected.
9. ForestGenerationId: ID representing the forest replication generation.
10. Row Number: Row number in the report.
11. UserMatchCount: How many users matched this record.
12. ValidUntil: When this data expires.
Category 3: Change Operation Context
13. DirSyncOperationType: Type of directory sync operation (add, modify, delete).
14. ModificationType: Type of change (add, modify, delete).
15. OriginatingServer: DC that made the change.
16. OriginatingTime: Time the change originated.
17. OriginatingUsers: User(s) who triggered the change.
18. OriginatingUserWorkstations: Workstations where change originated.
Category 4: Row Flags & Indicators
19. IsActionable: Whether this row requires action.
20. IsFirst: Whether this is the first change in a sequence.
21. IsLast: Whether this is the last change in a sequence.
22. IsPassword: Whether the change was to a password.
23. IsVirtual: Whether this is a virtual object.

## Filters available only for DNS reports
1. Zones: Active Directory DNS zones. Mandatory for DNS reports. Allowed states: This filter's only state is 'Include'. The input Can be 'Preset' or 'UserInput'. Allowed values: Closed list: The available Zones.
2. RecordTypes: DNS record types, defined in the DNS standards. Not mandatory. Allowed states: Can only be set to one of these: [Include, Exclude]. The input Can be 'Preset' or 'UserInput'. Allowed values: The ones still widely used today: A, NS, CNAME, SOA. May also include the historical ones.

## Display fields available only for DNS reports
Category 1: Object & Identity
1. AttributeName: Name of the changed attribute.
2. LastKnownParent: DN of the last known parent container.
3. LVRRef: Low version reference (version tracking).
4. SID: Security Identifier.
Category 5: Previous Value Metadata
5. From_IsStringValueXmlString: Whether the previous value was an XML string.
6. From_Meta_CreationTime: When this attribute value was created.
7. From_Meta_DeletionTime: When this attribute value was deleted.
8. From_Meta_HasData: Whether this field had data.
9. From_Meta_LastOriginatingChangeTime: When this value last changed.
10. From_Meta_LastOriginatingInvocationId: Invocation ID of the DC making the change.
11. From_Meta_LocalChangeUsn: Local USN when the change happened.
12. From_Meta_ObjectDn: DN of the object before change.
13. From_Meta_ObjectGuid: GUID of the object before change.
14. From_Meta_OriginatingChangeUsn: USN from the originating DC.
15. From_Meta_OriginatingServer: Server that originated the change.
16. From_Meta_Version: Version of the attribute value.
17. From_ResolveFlags: Flags describing resolution state.
18. From_Syntax: Data type of previous value.
Category 6: Previous Value Content
19. From_BinaryBase64Value: Previous binary value, Base64 encoded.
20. From_StringValue: Previous value as string.
Category 8: New Value Metadata
21. To_IsStringValueXmlString: Whether new value is XML string.
22. To_Meta_CreationTime: When this value was created.
23. To_Meta_DeletionTime: When this value was deleted.
24. To_Meta_HasData: Whether this field has data.
25. To_Meta_LastOriginatingChangeTime: When this value last changed.
26. To_Meta_LastOriginatingInvocationId: Invocation ID of the DC making the change.
27. To_Meta_LocalChangeUsn: Local USN when the change happened.
28. To_Meta_ObjectDn: DN after the change.
29. To_Meta_ObjectGuid: GUID after the change.
30. To_Meta_OriginatingChangeUsn: USN from the originating DC.
31. To_Meta_OriginatingServer: Server that originated the change.
32. To_Meta_Version: Version of the attribute.
33. To_ResolveFlags: Flags describing resolution state.
34. To_Syntax: Data type of new value.
Category 9: New Value Content
35. To_BinaryBase64Value: New binary value, Base64 encoded.
36. To_StringValue: New value as string.

## Filters available only for NonDNS reports
1. Partitions: Active Directory DNS partitions. Mandatory for NonDNS reports. Allowed states: Can only be set to one of these: [Include, Exclude]. The input Can be 'Preset' or 'UserInput'. Allowed values: Closed list: The available Partitions.
2. ObjectClasses: The AD object classes. Not mandatory. Allowed states: Can only be set to one of these: [Include, Exclude]. The input Can be 'Preset' or 'UserInput'. Allowed values: Multiple choice from all Active Directory object classes (e.g. aCSresourceLimits, applicationSettings, account, aCSPolicy...)
3. Attributes: The AD attributes. Not mandatory. Allowed states: Can only be set to one of these: [Include, Exclude]. The input Can be 'Preset' or 'UserInput'. Allowed values: Multiple choice from all Active Directory attribute names (e.g. accountNameHistory, accountExpires, aCSAggregateTokenRatePerUser…)
4. ObjectDN: The object's Distinguished Name. Not mandatory. Allowed states: Can only be set to one of these: [Equals, not equals, starts with]. The input Can be 'Preset' or 'UserInput'. Allowed values: Domain id.
5. GroupResultsByOperation: Should or shouldn't the results be grouped by the Operation? Not mandatory. Allowed states: Only state is 'Is'. The input Can be 'Preset' or 'UserInput'. Allowed values: true or false.
6. sAMAccountName: The user logon name, used for backwards compatibility with older versions of Windows. Not mandatory. Allowed states: Can only be set to one of these: [Equals, not equals, starts with, ends with]. The input Can be 'Preset' or 'UserInput'. Allowed values: Free text.---

# Display fields available only for NonDNS reports
Category 5: Previous Value Metadata
1. From_BinaryCheckSum: Checksum of previous binary data.
2. From_CheckSum: General checksum of previous value.
3. From_Flags: Flags on the previous record.
4. From_HasData: Whether previous record had data.
Category 6: Previous Value Content
5. From_RawBytesBase64: Previous raw bytes Base64 encoded.
Category 7: Previous DNS Record Details
6. From_Name: Previous DNS record name.
7. From_Record_Type: DNS record type before change.
8. From_Serial: Previous DNS serial number.
9. From_TextualForm: Previous DNS value in text.
10. From_TimeStamp: Timestamp of previous record.
11. From_TtlSeconds: Time to live in seconds.
12. From_TypeA_IPAddress: Previous A record IP.
13. From_TypeHInfoIsdnTxtX25Loc_StringData: Other string data for record types.
14. From_TypeMInfoRp_ErrorMailbox: MINFO record error mailbox.
15. From_TypeMInfoRp_Mailbox: MINFO record mailbox.
16. From_TypeMxAFSDBRt_NameExchange: MX/AFSDB exchange name.
17. From_TypeMxAFSDBRt_Preference: MX preference.
18. From_TypeName_Name: Record type name.
19. From_TypeSoa_Expire: SOA expire value.
20. From_TypeSoa_MinTtl: SOA minimum TTL.
21. From_TypeSoa_PrimaryServer: SOA primary server.
22. From_TypeSoa_Refresh: SOA refresh interval.
23. From_TypeSoa_Retry: SOA retry interval.
24. From_TypeSoa_ZoneAdministrator: SOA admin email.
25. From_TypeSrv_Host: SRV host.
26. From_TypeSrv_Port: SRV port.
27. From_TypeSrv_Priority: SRV priority.
28. From_TypeSrv_Weight: SRV weight.
29. From_TypeWks_Bitmask: WKS services bitmask.
30. From_TypeWks_IPAddress: WKS IP address.
31. From_TypeWks_Protocol: WKS protocol.
32. From_ZoneName: Previous DNS zone name.
Category 8: New Value Metadata
33. To_BinaryCheckSum: Checksum of new binary data.
34. To_CheckSum: General checksum of new value.
35. To_Flags: Flags on new record.
36. To_HasData: Whether new record has data.
Category 9: New Value Content
37. To_RawBytesBase64: New raw bytes Base64 encoded.
Category 10: New DNS Record Details
38. To_Name: New DNS record name.
39. To_RecordType: DNS record type after change.
40. To_Serial: New DNS serial number.
41. To_TextualForm: New DNS value in text.
42. To_TimeStamp: Timestamp of new record.
43. To_TtlSeconds: New TTL.
44. To_TypeA_IPAddress: New A record IP.
45. To_TypeHInfoIsdnTxtX25Loc_StringData: Other string data for record types.
46. To_TypeMInfoRp_ErrorMailbox: MINFO error mailbox.
47. To_TypeMInfoRp_Mailbox: MINFO mailbox.
48. To_TypeMxAFSDBRt_NameExchange: MX/AFSDB exchange name.
49. To_TypeMxAFSDBRt_Preference: MX preference.
50. To_TypeName_Name: Record type name.
51. To_TypeSoa_Expire: SOA expire value.
52. To_TypeSoa_MinTtl: SOA minimum TTL.
53. To_TypeSoa_PrimaryServer: SOA primary server.
54. To_TypeSoa_Refresh: SOA refresh interval.
55. To_TypeSoa_Retry: SOA retry interval.
56. To_TypeSoa_ZoneAdministrator: SOA admin email.
57. To_TypeSrv_Host: SRV host.
58. To_TypeSrv_Port: SRV port.
59. To_TypeSrv_Priority: SRV priority.
60. To_TypeSrv_Weight: SRV weight.
61. To_TypeWks_Bitmask: WKS services bitmask.
62. To_TypeWks_IPAddress: WKS IP address.
63. To_TypeWks_Protocol: WKS protocol.
64. To_ZoneName: New DNS zone name.

For each of these 3 kinds (LDAP, DNS, NonDNS), I'd like you look at the following XML report template- and tell me how likely it is to be of that kind.
For example:
If it might be LDAP, definitely not DNS and very likely NonDNS, then return: {result_example}.

Here's the report template:
<The XML file starts here>
{quest_report_str}
<The XML file ends here>

Here's your working process:
1. Read the report template.
2. Analyze the content of the report template.
3. Determine if the report is likely to be LDAP, DNS, or NonDNS based on the content.
4. Return a dictionary with keys "LDAP", "DNS", and "NonDNS" and values "yes", "no", or "maybe" based on your analysis.
5. You may add comments to your response in the designated fields.
"""
    return prompt


def complete_likelihoods(
    client, deployment_name, system_message, prompt, answer_format
):
    messages: List[Dict[str, Any]] = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": prompt},
    ]

    # Get the structured reply using the tool
    completion = client.chat.completions.create(
        model=deployment_name,
        messages=messages,
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "get_answering_schema",
                    "description": "Get the schema for the desired response based on user input.",
                    "parameters": answer_format.model_json_schema(),
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
    return parsed_json


def ask_user_for_type_confirmation(assumed_type: str, likelihood: str, reasoning: str):
    likelihood_phrasing = {
        "yes": "is very likely",
        "no": "is unlikely to be",
        "maybe": "might possibly be",
    }.get(likelihood, "unknown")
    statement = f"\n\nI think this report {likelihood_phrasing} of type '{assumed_type}', because {reasoning}."
    print(statement)
    user_input = input(
        "\nDo you agree? Enter 0 (no), 1 (maybe), or 2 (yes). Empty response=agree with my decision:\n"
    )

    the_user_thinks = {
        "0": "no",
        "1": "maybe",
        "2": "yes",
        "": likelihood,  # Empty response means agreement with the decision
    }

    if user_input not in the_user_thinks:
        print("Invalid input. Assuming agreement with the decision.")
        return the_user_thinks[user_input]
    if likelihood == the_user_thinks[user_input]:
        print("User agrees with the decision.")
    else:
        print("User disagrees with the decision.")

    print(f"User thinks: {the_user_thinks[user_input]}")
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
        result[key] = ask_user_for_type_confirmation(key, likelihood, reasoning)
    return parsed_completion


def get_likely_report_types(
    quest_report_str: str,
) -> Dict[Literal["LDAP", "DNS", "NonDNS"], Literal["yes", "no", "maybe"]]:
    # Analyze the quest_report_str and determine the likely report types
    # For now, we'll return a dummy implementation
    system_message = "You are a helpful assistant that analyzes a Reports and determines what kinds of report they could be."
    prompt = get_prompt_about_likely_report_types(quest_report_str)

    client, deployment_name = get_client_and_deployment_name()

    parsed_completion = complete_likelihoods(
        client, deployment_name, system_message, prompt, answer_format=ReportTypeHints
    )

    the_user_confirmed_likelihood = confirm_with_user(parsed_completion)

    return the_user_confirmed_likelihood
