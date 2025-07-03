from typing import Literal
from pydantic import BaseModel, Field
from schemas.Meta_schema import MetaSchema
from src.schemas.Content_schema import ContentSchema

class RATReportSchema(BaseModel):
    """Schema for RAT reports."""
    Content               : ContentSchema = Field(description="The content of the report")
    Meta                  : MetaSchema = Field(description="Metadata for the report")
    SecurityReportSettings: str = None
    CustomLogic           : str = None
