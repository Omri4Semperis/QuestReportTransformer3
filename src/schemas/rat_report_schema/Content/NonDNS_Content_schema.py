from pydantic import BaseModel, Field

from src.schemas.rat_report_schema.Content.Filters import NonDNS_Filter_schema
from src.schemas.rat_report_schema.Content.PreviewValues import NonDNS_PreviewValues_schema

class NonDNSContentSchema(BaseModel):
    """Schema for the actual content fields of RAT reports."""
    FilterString : str                         = None
    ResultColumns: NonDNS_ResultColumnSchema   = Field(default=None, description="How to present the results in this NonDNS report")
    Filter       : NonDNS_Filter_schema        = Field(description="The filtering settings used in this NonDNS report")
    PreviewValues: NonDNS_PreviewValues_schema = Field(description="How to preview the filtering values in this NonDNS report")