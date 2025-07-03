from typing import Dict, Literal, Optional, Union
from pydantic import BaseModel, Field

class DBPreviewValuesSchema(BaseModel):
    """
    "PreviewValues": (Dict[
        Literal[Available Filters for DNS or NonDNS, see bellow the full list of which filters are available for DNS vs. NonDNS reports],
        List[str] <-- contianing exactly one string, or None if not applicable
    ])
    A list of the preview (default) values to filter by that shall be presented on the report. e.g 'NonDNS' or 'DNS'; 'Abs:2025-06-02T06:58:51.4177807+00:00,2025-07-02T06:58:51.4177807+00:00', 'Create;Modify;Add;Remove;Move;Delete;Restore'; 'account;aCSPolicy;aCSResourceLimits;aCSSubnet;addressBookContainer;addressTemplate;applicationEntity;applicationProcess;applicationSettings;'; 'accountExpires;accountNameHistory;aCSAggregateTokenRatePerUser;aCSAllocableRSVPBandwidth;aCSCacheTimeout;aCSDirection;aCSDSBMDeadTime;aCSDSBMPriority;aCSDSBMRefresh;aCSEnableACSService;aCSEnableRSVPAccounting'; ':OU=engineering:True'; 'True'; etc
    """
    
    # NonDNS only filters
    - ObjectClasses
    - Partitions
    - Attributes
    - ObjectDN
    - GroupResultsByOperation
    - sAMAccountName

    # DNS only filter
    - Zones
    - RecordTypes
    
    # Both DNS and NonDNS filters
    - Type <- determines if the report is DNS or NonDNS
    - DateRange
    - Operations
    - OldValue
    - NewValue
    - ChangedBy
    - SourceServers
    - ObjectListIds