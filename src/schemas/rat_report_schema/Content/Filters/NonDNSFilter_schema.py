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
from src.schemas.rat_report_schema.Content.Filters.filter_fields.NonDNS_filter_fields import (
    NonDNSFilterField_Partitions,
    NonDNSFilterField_ObjectClasses,
    NonDNSFilterField_Attributes,
    NonDNSFilterField_ObjectDN,
    NonDNSFilterField_GroupResultsByOperation,
    NonDNSFilterField_sAMAccountName
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
        NonDNSFilterField_ObjectClasses,
        NonDNSFilterField_Attributes,
        NonDNSFilterField_ObjectDN,
        NonDNSFilterField_GroupResultsByOperation,
        NonDNSFilterField_sAMAccountName
    ]] = Field(description="A list of DB FilterField objects for the NonDNS report.")
    # TODO Type & Partitions are mandatory fields for NonDNS reports. Post process this field to include it in the list of all other fields.
    Type_field: Dict[str, str] = {"FieldName": "Type", "State": "Is", "Data": "NonDNS", "DataInputMethod": "Preset"}
    Partitions_field: NonDNSFilterField_Partitions = Field(description="The AD Partitions to filter by")