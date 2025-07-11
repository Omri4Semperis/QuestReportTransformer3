from typing import Literal
from pydantic import BaseModel, Field

from src.schemas.rat_report_schema.MetaData.Meta_schema import MetaDataSchema
from src.schemas.rat_report_schema.Content.NonDNS_Content_schema import NonDNSContentSchema

# TODO post processing- assert a 1:1 match between the filters fields used, also appear in PreviewValues
class NonDNSRATReportSchema(BaseModel):
    Meta                  : MetaDataSchema      = Field(description="Metadata for the report")
    Content               : NonDNSContentSchema = Field(description="The content of the report: Filters, display fields, etc.")
    # TODO these two indeed are always None
    SecurityReportSettings: str                 = None
    CustomLogic           : str                 = None