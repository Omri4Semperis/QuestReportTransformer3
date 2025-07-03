from typing import List, Literal, Optional, Union
from pydantic import BaseModel, Field

FilterField_FieldName_description = "Filter name. e.g. 'Type'; 'DateRange'; 'Operations'; 'sAMAccountName'; 'Partitions'; 'Zones'; 'RecordTypes'"
FilterField_State_description = "The relation of the data to the field."
FilterField_Data_description = "The value to check against. e.g. 'NonDNS'; 'Abs:2025-06-02T06:58:51.4177807+00:00,2025-07-02T06:58:51.4177807+00:00'; 'Create;Modify;Add;Remove'; 'account;aCSPolicy;aCSResourceLimits;aCSSubnet;addressBookContainer;addressTemplate;applicationEntity;'"
FilterField_DataInputMethod_description = "If Preset then a value (which is defined in PreviewValues field) is presented as a default and if UserInput then no default value is presented"

class FilterField(BaseModel):
    """
    FilterField schema (all fields are mandatory, non-nullable):
    {
        "FieldName"      : (str) Filter name. e.g. 'Type'; 'DateRange'; 'Operations'; 'sAMAccountName'; 'Partitions'; 'Zones'; 'RecordTypes',
        "State"          : (str) The relation of the data to the field. e.g. 'Is'; 'Exclude'; 'Include'; 'NotEquals'; 'NotContains'; 'StartsWith'; 'EndsWith',
        "Data"           : (str) The value to check against. e.g. 'NonDNS'; 'Abs:2025-06-02T06:58:51.4177807+00:00,2025-07-02T06:58:51.4177807+00:00'; 'Create;Modify;Add;Remove'; 'account;aCSPolicy;aCSResourceLimits;aCSSubnet;addressBookContainer;addressTemplate;applicationEntity;',
        "DataInputMethod": (Literal str: 'Preset' or 'UserInput') If Preset then a value (which is defined in PreviewValues field) is presented as a default and if UserInput then no default value is presented
    }
    """
    FieldName: str = Field(description=FilterField_FieldName_description)
    
    # TODO not all states go with all Fields. This data schema can be further specified,
    # so maybe introduce specific "FilterField"s classes, for each FieldName
    State: Literal["Is",
                   "Include", "Exclude",
                   "Equals", "NotEquals",
                   "StartsWith", "EndsWith",
                   "Contains", "NotContains"
                   "IsNotNullAndNotEmpty", "IsNullOrEmpty"] = Field(description=FilterField_State_description)
    
    Data: str = Field(description=FilterField_Data_description)
    
    DataInputMethod: Literal["Preset", "UserInput"] = Field(description=FilterField_DataInputMethod_description)

class DBFilterSchema(BaseModel):
    """
    Schema for the DB filter used in RAT reports:
    
    "Filter": (Dict[str, Union[str, List[Dict[str, str]]]]) {
        "$type": (str) always 'Semperis.ReportTemplates.DataSource.Data.DBFilterFields, Semperis.ReportTemplates.DataSource.Data',
        "FilterFields": (List[Dict[str, str]]) a list of DB FilterField. See bellow what an FilterField is
    },
    """
    DollarType: str = "Semperis.ReportTemplates.DataSource.Data.DBFilterFields, Semperis.ReportTemplates.DataSource.Data"
    FilterFields: List[FilterField] = Field(description="A list of DB FilterField objects")