from typing import List, Set, Union
from pydantic import BaseModel, Field

from schemas.rat_report_schema.Content.ResultColumns.DNS_ResultColumn_schema import DNSResultColumnSchema
from src.schemas.rat_report_schema.Content.Filters.DNS_Filter_schema import DNSFilterSchema
from src.schemas.rat_report_schema.Content.PreviewValues.Mutual_PreviewValues_schema import (
    MutualPreviewValue_DateRange,
    MutualPreviewValue_Operations,
    MutualPreviewValue_OldValue,
    MutualPreviewValue_NewValue,
    MutualPreviewValue_ChangedBy,
    MutualPreviewValue_SourceServers,
    MutualPreviewValue_ObjectListIds
)
from src.schemas.rat_report_schema.Content.PreviewValues.DNS_PreviewValues_schema import (
    DNSPreviewValue_Zones,
    DNSPreviewValue_RecordTypes
)

class DNSContentSchema(BaseModel):
    FilterString : str                         = None
    ResultColumns: List[DNSResultColumnSchema] = Field(default=None, description="How to present the results in this DNS report")
    Filter       : DNSFilterSchema             = Field(description="The filtering settings used in this DNS report")
    # TODO post processing- assert a 1:1 match between the filters fields used, also appear in PreviewValues
    # TODO post process this field into a list, and add the mandatory fields to it.
    PreviewValues: Set[Union[
        MutualPreviewValue_DateRange,
        MutualPreviewValue_Operations,
        MutualPreviewValue_OldValue,
        MutualPreviewValue_NewValue,
        MutualPreviewValue_ChangedBy,
        MutualPreviewValue_SourceServers,
        MutualPreviewValue_ObjectListIds,
        DNSPreviewValue_RecordTypes]]          = Field(description="How to preview the filtering values in this DNS report")
    # TODO post process to put the Zones field into the list of PreviewValues
    Zones: DNSPreviewValue_Zones               = Field(description="This field is mandatory for DNS reports and should be set to the Zones filter value.")