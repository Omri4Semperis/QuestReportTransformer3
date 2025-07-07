
from pydantic import BaseModel, Field


from src.schemas.rat_report_schema.Content.Filters.LDAP_Filter_schema import LDAPFilterSchema
from src.schemas.rat_report_schema.Content.PreviewValues.LDAP_PreviewValues_schema import LDAPPreviewValuesSchema

class LDAPContentSchema(BaseModel):
    FilterString : str                     = Field(default=None, description="The LDAP query as-is")
    ResultColumns: str                     = None
    Filter       : LDAPFilterSchema        = Field(description="The filter used in the report")
    PreviewValues: LDAPPreviewValuesSchema = Field(description="The Preview Values used in the report")