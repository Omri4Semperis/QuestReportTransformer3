from typing import Dict, List, Literal, Optional, Set, Union
from pydantic import BaseModel, Field
from src.schemas.rat_report_schema.Content.Filters.filter_fields.Mutual_filter_fields import (
    MutualFilterField_DateRange,
    MutualFilterField_Operations,
    MutualFilterField_OldValue,
    MutualFilterField_NewValue,
    MutualFilterField_ChangedBy,
    MutualFilterField_SourceServers,
    MutualFilterField_ObjectListIds
)
from src.schemas.rat_report_schema.Content.Filters.filter_fields.DNS_filter_fields import (
    DNSFilterField_Zones,
    DNSFilterField_RecordTypes
)

class DNSFilterSchema(BaseModel):
    # TODO post processing convert to $type
    DollarType: str = "Semperis.ReportTemplates.DataSource.Data.DBFilterFields, Semperis.ReportTemplates.DataSource.Data"
    # TODO Post process this field into a list, and add the mandatory fields to it.
    FilterFields: Set[Union[
        MutualFilterField_DateRange,
        MutualFilterField_Operations,
        MutualFilterField_OldValue,
        MutualFilterField_NewValue,
        MutualFilterField_ChangedBy,
        MutualFilterField_SourceServers,
        MutualFilterField_ObjectListIds,
        DNSFilterField_RecordTypes
    ]] = Field(description="A list of DB FilterField objects for the DNS report.")
    # TODO Type & Zones are mandatory fields for DNS reports. Post process this field to include it in the list of all other fields.
    Type_field: Dict[str, str] = {"FieldName": "Type", "State": "Is", "Data": "DNS", "DataInputMethod": "Preset"}
    Zones_field: DNSFilterField_Zones = Field(description="The DNS zones to filter by")