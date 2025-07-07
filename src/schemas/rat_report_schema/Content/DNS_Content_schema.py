from typing import List
from pydantic import BaseModel, Field

from schemas.rat_report_schema.Content.ResultColumns.DNS_ResultColumn_schema import DNSResultColumnSchema
from src.schemas.rat_report_schema.Content.Filters import DNS_Filter_schema
from src.schemas.rat_report_schema.Content.PreviewValues import DNS_PreviewValues_schema

class DNSContentSchema(BaseModel):
    """Schema for the actual content fields of RAT reports."""
    FilterString : str                         = None
    ResultColumns: List[DNSResultColumnSchema] = Field(default=None, description="How to present the results in this DNS report")
    Filter       : DNS_Filter_schema           = Field(description="The filtering settings used in this DNS report")
    PreviewValues: DNS_PreviewValues_schema    = Field(description="How to preview the filtering values in this DNS report")