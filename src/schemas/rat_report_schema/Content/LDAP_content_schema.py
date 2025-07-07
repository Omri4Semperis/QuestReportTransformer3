from typing import Literal, Optional, Union
from pydantic import BaseModel, Field

from src.schemas.rat_report_schema.Content.Filters.LDAPFilter_schema import LDAPFilterSchema
from src.schemas.rat_report_schema.Content.PreviewValues.LDAPPreviewValues_schema import LDAPPreviewValuesSchema


class ContentSchema(BaseModel):
    """Schema for the actual content fields of RAT reports."""

    Filter:        LDAPFilterSchema        = Field(description="The filter used in the report")
    PreviewValues: LDAPPreviewValuesSchema = Field(description="The Preview Values used in the report, either LDAP or DB")
    FilterString:  str                     = Field(default=None, description="If report source is LDAP then this is the LDAP query as-is. Else- None",)
    ResultColumns: str                     = None