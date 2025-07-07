from typing import Literal

mutual_filters = """# Filters available for both DNS and NonDNS reports
1. Type: Determines if the report is DNS or NonDNS. Mandatory for both DNS and NonDNS. Allowed states: Only state is 'Is'. The input Can only be 'Preset'. Allowed values: DNS or NonDNS.
2. DateRange: The date range to consider. Not mandatory. Allowed states: Only state is 'Is'. The input Can be 'Preset' or 'UserInput'. Allowed values: Can be relative or absolute.
3. Operations: The types of AD operations. Not mandatory. Allowed states: Can only be set to one of these: [Include, Exclude]. The input Can be 'Preset' or 'UserInput'. Allowed values: Multiple choice from: Create, Modify, Add, Remove, Move, Delete, Restore
4. OldValue: The old value of the object's attirubute. Not mandatory. Allowed states: Can only be set to one of these: [Contains, NotContain, Equals, NotEquals IsNotNullAndNotEmpty, IsNullOrEmpty]. The input Can be 'Preset' or 'UserInput'. Allowed values: Free text.
5. NewValue: The new value of the object's attirubute. Not mandatory. Allowed states: Can only be set to one of these: [Contains, NotContain, Equals, NotEquals IsNotNullAndNotEmpty, IsNullOrEmpty]. The input Can be 'Preset' or 'UserInput'. Allowed values: Free text.
6. ChangedBy: The value of the object that caused the change. Not mandatory. Allowed states: Can only be set to one of these: [Contains, NotContain, Equals, NotEquals IsNotNullAndNotEmpty, IsNullOrEmpty]. The input Can be 'Preset' or 'UserInput'. Allowed values: Free text.
7. SourceServers: Domain controllers or DNS servers that are the source of the data Not mandatory. Allowed states: Can only be set to one of these: [Include, Exclude]. The input Can be 'Preset' or 'UserInput'. Allowed values: Closed list: The available Source Servers.
8. ObjectListIds: internal identifiers or unique IDs. Not mandatory. Allowed states: Can only be set to one of these: [Equals, not equals, starts with, ends with]. The input Can be 'Preset' or 'UserInput'. Allowed values: Free text."""

mutual_displays = """# Display fields available for both DNS and NonDNS reports
## Category 1: Object & Identity
1. ClassName: Object class (e.g., user, group, computer).
2. DisplayName: User-friendly display name.
3. Distinguished Name: Full LDAP path identifying the object.
4. Object Guid: Unique GUID of the object.
5. SamAccountName: Pre-Windows 2000 logon name.
6. UPN: User Principal Name (user@domain).
7. Version: Version of the record.
## Category 2: Report & Collection Metadata
8. CollectionTime: When the data was collected.
9. ForestGenerationId: ID representing the forest replication generation.
10. Row Number: Row number in the report.
11. UserMatchCount: How many users matched this record.
12. ValidUntil: When this data expires.
## Category 3: Change Operation Context
13. DirSyncOperationType: Type of directory sync operation (add, modify, delete).
14. ModificationType: Type of change (add, modify, delete).
15. OriginatingServer: DC that made the change.
16. OriginatingTime: Time the change originated.
17. OriginatingUsers: User(s) who triggered the change.
18. OriginatingUserWorkstations: Workstations where change originated.
## Category 4: Row Flags & Indicators
19. IsActionable: Whether this row requires action.
20. IsFirst: Whether this is the first change in a sequence.
21. IsLast: Whether this is the last change in a sequence.
22. IsPassword: Whether the change was to a password.
23. IsVirtual: Whether this is a virtual object."""

only_dns_filters: str = """# Filters available only for DNS reports
1. Zones: Active Directory DNS zones. Mandatory for DNS reports. Allowed states: This filter's only state is 'Include'. The input Can be 'Preset' or 'UserInput'. Allowed values: Closed list: The available Zones.
2. RecordTypes: DNS record types, defined in the DNS standards. Not mandatory. Allowed states: Can only be set to one of these: [Include, Exclude]. The input Can be 'Preset' or 'UserInput'. Allowed values: The ones still widely used today: A, NS, CNAME, SOA. May also include the historical ones."""

only_nondns_filters: str = """# Filters available only for NonDNS reports
1. Partitions: Active Directory DNS partitions. Mandatory for NonDNS reports. Allowed states: Can only be set to one of these: [Include, Exclude]. The input Can be 'Preset' or 'UserInput'. Allowed values: Closed list: The available Partitions.
2. ObjectClasses: The AD object classes. Not mandatory. Allowed states: Can only be set to one of these: [Include, Exclude]. The input Can be 'Preset' or 'UserInput'. Allowed values: Multiple choice from all Active Directory object classes (e.g. aCSresourceLimits, applicationSettings, account, aCSPolicy...)
3. Attributes: The AD attributes. Not mandatory. Allowed states: Can only be set to one of these: [Include, Exclude]. The input Can be 'Preset' or 'UserInput'. Allowed values: Multiple choice from all Active Directory attribute names (e.g. accountNameHistory, accountExpires, aCSAggregateTokenRatePerUser…)
4. ObjectDN: The object's Distinguished Name. Not mandatory. Allowed states: Can only be set to one of these: [Equals, not equals, starts with]. The input Can be 'Preset' or 'UserInput'. Allowed values: Domain id.
5. GroupResultsByOperation: Should or shouldn't the results be grouped by the Operation? Not mandatory. Allowed states: Only state is 'Is'. The input Can be 'Preset' or 'UserInput'. Allowed values: true or false.
6. sAMAccountName: The user logon name, used for backwards compatibility with older versions of Windows. Not mandatory. Allowed states: Can only be set to one of these: [Equals, not equals, starts with, ends with]. The input Can be 'Preset' or 'UserInput'. Allowed values: Free text."""

only_dns_displays: str = """# Display fields available only for DNS reports
## Category 1: Object & Identity
1. AttributeName: Name of the changed attribute.
2. LastKnownParent: DN of the last known parent container.
3. LVRRef: Low version reference (version tracking).
4. SID: Security Identifier.
## Category 5: Previous Value Metadata
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
## Category 6: Previous Value Content
19. From_BinaryBase64Value: Previous binary value, Base64 encoded.
20. From_StringValue: Previous value as string.
## Category 8: New Value Metadata
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
## Category 9: New Value Content
35. To_BinaryBase64Value: New binary value, Base64 encoded.
36. To_StringValue: New value as string."""

only_nondns_displays: str = """# Display fields available only for NonDNS reports
## Category 5: Previous Value Metadata
1. From_BinaryCheckSum: Checksum of previous binary data.
2. From_CheckSum: General checksum of previous value.
3. From_Flags: Flags on the previous record.
4. From_HasData: Whether previous record had data.
## Category 6: Previous Value Content
5. From_RawBytesBase64: Previous raw bytes Base64 encoded.
## Category 7: Previous DNS Record Details
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
## Category 8: New Value Metadata
33. To_BinaryCheckSum: Checksum of new binary data.
34. To_CheckSum: General checksum of new value.
35. To_Flags: Flags on new record.
36. To_HasData: Whether new record has data.
## Category 9: New Value Content
37. To_RawBytesBase64: New raw bytes Base64 encoded.
## Category 10: New DNS Record Details
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
64. To_ZoneName: New DNS zone name."""


def describe_report_properties(
    report_type: Literal["NDS", "DNS", "both"],
    filters_or_displays: Literal["filters", "displays", "both"],
) -> str:
    """Returns a description of the properties of the given report type."""
    res = ""
    if report_type == "both":
        if filters_or_displays == "filters" or filters_or_displays == "both":
            res += "\n".join(
                [
                    "Here are the filters available for both DNS and NonDNS reports:",
                    mutual_filters,
                    "Here are the filters available only for DNS reports:",
                    only_dns_filters,
                    "Here are the filters available only for NonDNS reports:",
                    only_nondns_filters,
                    "\n",
                ]
            )
        elif filters_or_displays == "displays" or filters_or_displays == "both":
            res += "\n".join(
                [
                    "Here are the display fields available for both DNS and NonDNS reports:",
                    mutual_displays,
                    "Here are the display fields available only for DNS reports:",
                    only_dns_displays,
                    "Here are the display fields available only for NonDNS reports:",
                    only_nondns_displays,
                    "\n",
                ]
            )
    elif report_type == "NDS":
        if filters_or_displays == "filters" or filters_or_displays == "both":
            res += "\n".join([mutual_filters, only_dns_filters])
        elif filters_or_displays == "displays" or filters_or_displays == "both":
            res += "\n".join([mutual_displays, only_dns_displays])
    elif report_type == "DNS":
        if filters_or_displays == "filters" or filters_or_displays == "both":
            res += "\n".join([mutual_filters, only_nondns_filters])
        elif filters_or_displays == "displays" or filters_or_displays == "both":
            res += "\n".join([mutual_displays, only_nondns_displays])

    return res


def describe_LDAP() -> str:
    return """# LDAP Report Properties:
An LDAP report is about Active Directory state, such as user accounts, groups, and organizational units.
It can only be about the current state of Active Directory, not historical changes.
It is typically used to query information that can be retrieved using LDAP queries.
For example, it can be used to find all users in a specific group or to retrieve the attributes of a specific user.

LDAP queries can be short or long. Here are a few examples of LDAP queries:
Find all objects with objectClass = user: (&(objectClass=user))
Find user objects whose login name is jdoe: (&(objectClass=user)(sAMAccountName=jdoe))
Return all group objects: (objectClass=group)
Return users where the disabled flag is NOT set: (&(objectClass=user)(!(userAccountControl:1.2.840.113556.1.4.803:=2)))
Return users who belong to the Admins group: (&(objectClass=user)(memberOf=CN=Admins,CN=Users,DC=example,DC=com))"""
