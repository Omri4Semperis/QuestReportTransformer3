from typing import Literal
from pydantic import BaseModel, Field
from schemas.MetaData.Meta_schema import MetaSchema
from schemas.Content.Content_schema import ContentSchema

class RATReportSchema(BaseModel):
    """Schema for RAT reports."""
    Meta                  : MetaSchema = Field(description="Metadata for the report")
    Content               : ContentSchema = Field(description="The content of the report: Filters, display fields, etc.")
    SecurityReportSettings: str = None
    CustomLogic           : str = None
