from typing import Dict, List, Literal, Optional, Union
from pydantic import BaseModel, Field

# Field descriptions for DB preview values
DBPreviewValuesSchema_ObjectClasses_description = "Preview values for ObjectClasses filter (NonDNS only)"
DBPreviewValuesSchema_Partitions_description = "Preview values for Partitions filter (NonDNS only)"
DBPreviewValuesSchema_Attributes_description = "Preview values for Attributes filter (NonDNS only)"
DBPreviewValuesSchema_ObjectDN_description = "Preview values for ObjectDN filter (NonDNS only)"
DBPreviewValuesSchema_GroupResultsByOperation_description = "Preview values for GroupResultsByOperation filter (NonDNS only)"
DBPreviewValuesSchema_sAMAccountName_description = "Preview values for sAMAccountName filter (NonDNS only)"
DBPreviewValuesSchema_Zones_description = "Preview values for Zones filter (DNS only)"
DBPreviewValuesSchema_RecordTypes_description = "Preview values for RecordTypes filter (DNS only)"
DBPreviewValuesSchema_Type_description = "Preview values for Type filter - determines if the report is DNS or NonDNS (both DNS and NonDNS)"
DBPreviewValuesSchema_DateRange_description = "Preview values for DateRange filter (both DNS and NonDNS)"
DBPreviewValuesSchema_Operations_description = "Preview values for Operations filter (both DNS and NonDNS)"
DBPreviewValuesSchema_OldValue_description = "Preview values for OldValue filter (both DNS and NonDNS)"
DBPreviewValuesSchema_NewValue_description = "Preview values for NewValue filter (both DNS and NonDNS)"
DBPreviewValuesSchema_ChangedBy_description = "Preview values for ChangedBy filter (both DNS and NonDNS)"
DBPreviewValuesSchema_SourceServers_description = "Preview values for SourceServers filter (both DNS and NonDNS)"
DBPreviewValuesSchema_ObjectListIds_description = "Preview values for ObjectListIds filter (both DNS and NonDNS)"

class DBPreviewValuesSchema(BaseModel):
    """
    Schema for DB Preview Values in RAT reports.
    
    "PreviewValues": (Dict[
        Literal[Available Filters for DNS or NonDNS, see below the full list of which filters are available for DNS vs. NonDNS reports],
        List[str] <-- containing exactly one string, or None if not applicable
    ])
    
    A list of the preview (default) values to filter by that shall be presented on the report. 
    Examples: 'NonDNS' or 'DNS'; 'Abs:2025-06-02T06:58:51.4177807+00:00,2025-07-02T06:58:51.4177807+00:00'; 
    'Create;Modify;Add;Remove;Move;Delete;Restore'; 'account;aCSPolicy;aCSResourceLimits;aCSSubnet;addressBookContainer;addressTemplate;applicationEntity;applicationProcess;applicationSettings;'; 
    'accountExpires;accountNameHistory;aCSAggregateTokenRatePerUser;aCSAllocableRSVPBandwidth;aCSCacheTimeout;aCSDirection;aCSDSBMDeadTime;aCSDSBMPriority;aCSDSBMRefresh;aCSEnableACSService;aCSEnableRSVPAccounting'; 
    ':OU=engineering:True'; 'True'; etc
    """
    
    # NonDNS only filters
    ObjectClasses: Optional[List[str]] = Field(default=None, description=DBPreviewValuesSchema_ObjectClasses_description)
    Partitions: Optional[List[str]] = Field(default=None, description=DBPreviewValuesSchema_Partitions_description)
    Attributes: Optional[List[str]] = Field(default=None, description=DBPreviewValuesSchema_Attributes_description)
    ObjectDN: Optional[List[str]] = Field(default=None, description=DBPreviewValuesSchema_ObjectDN_description)
    GroupResultsByOperation: Optional[List[str]] = Field(default=None, description=DBPreviewValuesSchema_GroupResultsByOperation_description)
    sAMAccountName: Optional[List[str]] = Field(default=None, description=DBPreviewValuesSchema_sAMAccountName_description)

    # DNS only filters
    Zones: Optional[List[str]] = Field(default=None, description=DBPreviewValuesSchema_Zones_description)
    RecordTypes: Optional[List[str]] = Field(default=None, description=DBPreviewValuesSchema_RecordTypes_description)
    
    # Both DNS and NonDNS filters
    Type: Optional[List[str]] = Field(default=None, description=DBPreviewValuesSchema_Type_description)  # determines if the report is DNS or NonDNS
    DateRange: Optional[List[str]] = Field(default=None, description=DBPreviewValuesSchema_DateRange_description)
    Operations: Optional[List[str]] = Field(default=None, description=DBPreviewValuesSchema_Operations_description)
    OldValue: Optional[List[str]] = Field(default=None, description=DBPreviewValuesSchema_OldValue_description)
    NewValue: Optional[List[str]] = Field(default=None, description=DBPreviewValuesSchema_NewValue_description)
    ChangedBy: Optional[List[str]] = Field(default=None, description=DBPreviewValuesSchema_ChangedBy_description)
    SourceServers: Optional[List[str]] = Field(default=None, description=DBPreviewValuesSchema_SourceServers_description)
    ObjectListIds: Optional[List[str]] = Field(default=None, description=DBPreviewValuesSchema_ObjectListIds_description)