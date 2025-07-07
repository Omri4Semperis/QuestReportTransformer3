from pydantic import BaseModel, Field

"""# Filters available for both DNS and NonDNS reports
1. Type: Determines if the report is DNS or NonDNS. Mandatory for both DNS and NonDNS. Allowed states: Only state is 'Is'. The input Can only be 'Preset'. Allowed values: DNS or NonDNS.
2. DateRange: The date range to consider. Not mandatory. Allowed states: Only state is 'Is'. The input Can be 'Preset' or 'UserInput'. Allowed values: Can be relative or absolute.
3. Operations: The types of AD operations. Not mandatory. Allowed states: Can only be set to one of these: [Include, Exclude]. The input Can be 'Preset' or 'UserInput'. Allowed values: Multiple choice from: Create, Modify, Add, Remove, Move, Delete, Restore
4. OldValue: The old value of the object's attirubute. Not mandatory. Allowed states: Can only be set to one of these: [Contains, NotContain, Equals, NotEquals IsNotNullAndNotEmpty, IsNullOrEmpty]. The input Can be 'Preset' or 'UserInput'. Allowed values: Free text.
5. NewValue: The new value of the object's attirubute. Not mandatory. Allowed states: Can only be set to one of these: [Contains, NotContain, Equals, NotEquals IsNotNullAndNotEmpty, IsNullOrEmpty]. The input Can be 'Preset' or 'UserInput'. Allowed values: Free text.
6. ChangedBy: The value of the object that caused the change. Not mandatory. Allowed states: Can only be set to one of these: [Contains, NotContain, Equals, NotEquals IsNotNullAndNotEmpty, IsNullOrEmpty]. The input Can be 'Preset' or 'UserInput'. Allowed values: Free text.
7. SourceServers: Domain controllers or DNS servers that are the source of the data Not mandatory. Allowed states: Can only be set to one of these: [Include, Exclude]. The input Can be 'Preset' or 'UserInput'. Allowed values: Closed list: The available Source Servers.
8. ObjectListIds: internal identifiers or unique IDs. Not mandatory. Allowed states: Can only be set to one of these: [Equals, not equals, starts with, ends with]. The input Can be 'Preset' or 'UserInput'. Allowed values: Free text."""

# TODO post process to a single value in a list

class MutualPreviewValue_DateRange(BaseModel):
    value: str = Field(description="The date range to consider. Same as the Data of the DateRangefilter, if was used.")

class MutualPreviewValue_Operations(BaseModel):
    value: str = Field(description="The type of AD operations to consider. Same as the Data of the Operations filter, if was used.")
    
class MutualPreviewValue_OldValue(BaseModel):
    value: str = Field(description="The old value of the object's attribute. Same as the Data of the OldValue filter, if was used.")

class MutualPreviewValue_NewValue(BaseModel):
    value: str = Field(description="The new value of the object's attribute. Same as the Data of the NewValue filter, if was used.")

class MutualPreviewValue_ChangedBy(BaseModel):
    value: str = Field(description="The value of the object that caused the change. Same as the Data of the ChangedBy filter, if was used.")
    
class MutualPreviewValue_SourceServers(BaseModel):
    value: str = Field(description="The source servers that are the source of the data. Same as the Data of the SourceServers filter, if was used.")
    
class MutualPreviewValue_ObjectListIds(BaseModel):
    value: str = Field(description="The internal identifiers or unique IDs. Same as the Data of the ObjectListIds filter, if was used.")