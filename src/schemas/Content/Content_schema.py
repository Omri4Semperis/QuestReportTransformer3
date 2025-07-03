from typing import Literal, Optional, Union
from pydantic import BaseModel, Field

from schemas.Content.Filters.LDAPFilter_schema import LDAPFilterSchema
from schemas.Content.Filters.DBFilter_schema import DBFilterSchema
from schemas.Content.PreviewValues.LDAPPreviewValues_schema import LDAPPreviewValuesSchema


ContentSchema_FilterString_description  = "If report source is LDAP then this is the LDAP query as-is. Else- None"
ContentSchema_Filter_description        = "The filter used in the report, either LDAP or DB"
ContentSchema_PreviewValues_description = "The Preview Values used in the report, either LDAP or DB"
ContentSchema_ResultColumns_description = "If report source is DB then this is the ResultColumnsSchema for DB. Else- None."

class ContentSchema(BaseModel):
    """Schema for the actual content fields of RAT reports."""
    
    Filter       : Union[LDAPFilterSchema, DBFilterSchema]               = Field(description=ContentSchema_Filter_description)
    PreviewValues: Union[
        LDAPPreviewValuesSchema,
        DBPreviewValuesSchema
    ] = Field(description=ContentSchema_PreviewValues_description)
    FilterString : Optional[str]                                         = Field(default=None, description=ContentSchema_FilterString_description)
    ResultColumns: Optional[ResultColumnsSchema]                         = Field(default=None, description=ContentSchema_ResultColumns_description)
