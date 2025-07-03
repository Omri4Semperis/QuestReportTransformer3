from typing import Dict, Literal, Optional, Union, List
from pydantic import BaseModel, Field

class DBPreviewValuesSchema(BaseModel):
    """
    "PreviewValues": (Dict[
        Literal[Available Filters for DNS or NonDNS, see bellow the full list of which filters are available for DNS vs. NonDNS reports],
        List[str] <-- contianing exactly one string, or None if not applicable
    ])
    A list of the preview (default) values to filter by that shall be presented on the report. e.g 'NonDNS' or 'DNS'; 'Abs:2025-06-02T06:58:51.4177807+00:00,2025-07-02T06:58:51.4177807+00:00', 'Create;Modify;Add;Remove;Move;Delete;Restore'; 'account;aCSPolicy;aCSResourceLimits;aCSSubnet;addressBookContainer;addressTemplate;applicationEntity;applicationProcess;applicationSettings;'; 'accountExpires;accountNameHistory;aCSAggregateTokenRatePerUser;aCSAllocableRSVPBandwidth;aCSCacheTimeout;aCSDirection;aCSDSBMDeadTime;aCSDSBMPriority;aCSDSBMRefresh;aCSEnableACSService;aCSEnableRSVPAccounting'; ':OU=engineering:True'; 'True'; etc
    """
    # Both DNS and NonDNS filters
    Type         : Literal["DNS", "NonDNS"] = Field(description="Mandatory field. Determines if the report is DNS or NonDNS")
    DateRange    : Optional[str]            = Field(description="A string representing the date range in ISO 8601 format if absolute or by Semperis syntax if relative. e.g. 'Abs:2025-06-02T07:16:56.9737401+00:00,2025-07-02T07:16:56.9737401+00:00' or 'Rel:1D' (last 1 day) or 'Rel:7W' (last 7 weeks) or 'Rel:2M' (last 2 months) ")
    OldValue     : Optional[str]            = Field(default=None, description="The old value of the attribute that was changed.")
    NewValue     : Optional[str]            = Field(default=None, description="The new value of the attribute that was changed.")
    ChangedBy    : Optional[str]            = Field(default=None, description="The text of the entity that made the change.")  # TODO understand what this means
    SourceServers: Optional[List[str]]      = Field(default=None, description="A list of source servers that are relevant for the report. e.g. ['server1', 'server2']")  # TODO understand what this means
    ObjectListIds: Optional[List[str]]      = Field(default=None, description="A list of object IDs that are relevant for the report. e.g. ['object1', 'object2']")  # TODO understand what this means
    Operations   : Optional[List[Literal["Create", "Modify", "Add", "Remove", "Move", "Delete", "Restore"]]] = Field(default=None, description="All operations that are relevant for the report. e.g. ['Create', 'Modify', 'Add', 'Remove', 'Move', 'Delete', 'Restore']")
    
    # NonDNS only filters
    Partitions             : List[str]           = Field(description="Mandatory field. A list of partitions that are relevant for the report. e.g. ['CN=Configuration,DC=d01,DC=lab', 'CN=Schema,CN=Configuration,DC=d01,DC=lab;DC=d01,DC=lab', 'DC=d02,DC=d01,DC=lab', 'DC=DomainDnsZones,DC=d01,DC=lab', 'DC=DomainDnsZones,DC=d02,DC=d01,DC=lab;DC=ForestDnsZones,DC=d01,DC=lab']")  # TODO understand what this means, where is it from
    sAMAccountName         : Optional[str]       = Field(default=None, description="sAMAccountName to filter the report on")
    ObjectDN               : Optional[str]       = Field(default=None, description="Of the form ':<A DN without Partition or Domain>:<True/False to include Child Objects>' e.g. ':OU=engineering:True'")
    GroupResultsByOperation: Optional[bool]      = Field(default=None, description="Whether to group results by operation.")
    ObjectClasses          : Optional[List[str]] = Field(default=None, description="A list of object classes that are relevant for the report. e.g. ['account', 'aCSPolicy', 'aCSResourceLimits', 'aCSSubnet', 'addressBookContainer', 'addressTemplate', 'applicationEntity', 'applicationProcess', 'applicationSettings', 'applicationSiteSettings']")
    Attributes             : Optional[List[str]] = Field(default=None, description="A list of attributes that are relevant for the report. e.g. ['accountExpires', 'accountNameHistory', 'aCSAggregateTokenRatePerUser', 'aCSAllocableRSVPBandwidth', 'aCSCacheTimeout', 'aCSDirection', 'aCSDSBMDeadTime']")

    # DNS only filter
    Zones      : List[str] = Field(description="Mandatory field. A list of DNS zones that are relevant for the report. e.g. ['..TrustAnchors (DC=ForestDnsZones,DC=d01,DC=lab)', '_msdcs.d01.lab (DC=ForestDnsZones,DC=d01,DC=lab)', 'd01.lab (DC=DomainDnsZones,DC=d01,DC=lab)', 'd02.d01.lab (DC=DomainDnsZones,DC=d02,DC=d01,DC=lab)']")  # TODO understand what this means, where is it from
    RecordTypes: List[str] = Field(description="Mandatory field. A list of DNS record types that are relevant for the report. e.g. ['ZERO', 'A', 'NS', 'MD', 'MF', 'CNAME', 'SOA', 'MB', 'MG', 'MR', 'NULL', 'WKS', 'PTR', 'HINFO', 'MINFO', 'MX', 'TXT', 'RP', 'AFSDB', 'X25', 'ISDN', 'RT', 'SIG', 'KEY', 'AAAA', 'LOC', 'NXT', 'SRV', 'ATMA', 'NAPTR', 'DNAME', 'DS', 'SSHFP', 'RRSIG', 'NSEC', 'DNSKEY', 'DHCID', 'NSEC3', 'NSEC3PARAM', 'ALL', 'WINS', 'WINSR', 'ZONE']")  # TODO understand what this means, where is it from
    
# TODO Fields with None values should be removed.
# TODO This schema requires post-processing: All values of these fields are of different types, but should be lists of a single string object formatted in different ways.