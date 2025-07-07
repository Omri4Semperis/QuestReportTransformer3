from typing import List, Set, Union
from pydantic import BaseModel, Field

from schemas.rat_report_schema.Content.ResultColumns.NonDNS_ResultColumn_schema import NonDNSResultColumnSchema
from src.schemas.rat_report_schema.Content.Filters.NonDNS_Filter_schema import NonDNSFilterSchema
from src.schemas.rat_report_schema.Content.PreviewValues.Mutual_PreviewValues_schema import (
    MutualPreviewValue_DateRange,
    MutualPreviewValue_Operations,
    MutualPreviewValue_OldValue,
    MutualPreviewValue_NewValue,
    MutualPreviewValue_ChangedBy,
    MutualPreviewValue_SourceServers,
    MutualPreviewValue_ObjectListIds
)
from src.schemas.rat_report_schema.Content.PreviewValues.NonDNS_PreviewValues_schema import (
    NonDNSPreviewValue_Partitions,
    NonDNSPreviewValue_ObjectClasses,
    NonDNSPreviewValue_Attributes,
    NonDNSPreviewValue_ObjectDN,
    NonDNSPreviewValue_GroupResultsByOperation,
    NonDNSPreviewValue_sAMAccountName
)
    

class NonDNSContentSchema(BaseModel):
    FilterString : str                            = None
    ResultColumns: List[NonDNSResultColumnSchema] = Field(default=None, description="How to present the results in this NonDNS report")
    Filter       : NonDNSFilterSchema             = Field(description="The filtering settings used in this NonDNS report")
    # TODO post processing- assert a 1:1 match between the filters fields used, also appear in PreviewValues
    # TODO post process this field into a list, and add the mandatory fields to it.
    PreviewValues: Set[Union[
        MutualPreviewValue_DateRange,
        MutualPreviewValue_Operations,
        MutualPreviewValue_OldValue,
        MutualPreviewValue_NewValue,
        MutualPreviewValue_ChangedBy,
        MutualPreviewValue_SourceServers,
        MutualPreviewValue_ObjectListIds,
        NonDNSPreviewValue_ObjectClasses,
        NonDNSPreviewValue_Attributes,
        NonDNSPreviewValue_ObjectDN,
        NonDNSPreviewValue_GroupResultsByOperation,
        NonDNSPreviewValue_sAMAccountName]]      = Field(description="How to preview the filtering values in this NonDNS report")
    # TODO post process to put the Partitions field into the list of PreviewValues
    Partitions: NonDNSPreviewValue_Partitions    = Field(description="This field is mandatory for NonDNS reports and should be set to the Partitions filter value.")