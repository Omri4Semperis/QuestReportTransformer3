from typing import Literal, Optional
from pydantic import BaseModel, Field

class ContentSchema(BaseModel):
    """Schema for the actual content fields of RAT reports."""
    
    FilterString: Optional[str] = Field(
        description="If report source is LDAP then this is the LDAP query as-is. Else- None")
    
    Filter: Literal[
        LDAPFilterSchema,
        DBFilterSchema
        ] = Field(
            description="The filter used in the report, either LDAP or DB")
    
    PreviewValues: Literal[
        LDAPPreviewValuesSchema,
        DBPreviewValuesSchema
        ] = Field(
            description="The Preview Values used in the report, either LDAP or DB")
    
    ResultColumns: Optional[ResultColumnsSchema] = Field(
        default=None,
        description=f"If report source is DB then this is the ResultColumnsSchema for DB. Else- None.")
