from pydantic import BaseModel, Field

"""# Filters available only for NonDNS reports
1. Partitions: Active Directory DNS partitions. Mandatory for NonDNS reports. Allowed states: Can only be set to one of these: [Include, Exclude]. The input Can be 'Preset' or 'UserInput'. Allowed values: Closed list: The available Partitions.
2. ObjectClasses: The AD object classes. Not mandatory. Allowed states: Can only be set to one of these: [Include, Exclude]. The input Can be 'Preset' or 'UserInput'. Allowed values: Multiple choice from all Active Directory object classes (e.g. aCSresourceLimits, applicationSettings, account, aCSPolicy...)
3. Attributes: The AD attributes. Not mandatory. Allowed states: Can only be set to one of these: [Include, Exclude]. The input Can be 'Preset' or 'UserInput'. Allowed values: Multiple choice from all Active Directory attribute names (e.g. accountNameHistory, accountExpires, aCSAggregateTokenRatePerUser…)
4. ObjectDN: The object's Distinguished Name. Not mandatory. Allowed states: Can only be set to one of these: [Equals, not equals, starts with]. The input Can be 'Preset' or 'UserInput'. Allowed values: Domain id.
5. GroupResultsByOperation: Should or shouldn't the results be grouped by the Operation? Not mandatory. Allowed states: Only state is 'Is'. The input Can be 'Preset' or 'UserInput'. Allowed values: true or false.
6. sAMAccountName: The user logon name, used for backwards compatibility with older versions of Windows. Not mandatory. Allowed states: Can only be set to one of these: [Equals, not equals, starts with, ends with]. The input Can be 'Preset' or 'UserInput'. Allowed values: Free text."""

# TODO post process to a single value in a list

class MutualPreviewValue_Partitions(BaseModel):
    value: str = Field(description="Active Directory DNS partitions. Same as the Data in the Partitions filter, if was used.")
    
class MutualPreviewValue_ObjectClasses(BaseModel):
    value: str = Field(description="The AD object classes to consider. Same as the Data in the ObjectClasses filter, if was used.")

class MutualPreviewValue_Attributes(BaseModel):
    value: str = Field(description="The AD attributes to consider. Same as the Data in the Attributes filter, if was used.")

class MutualPreviewValue_ObjectDN(BaseModel):
    value: str = Field(description="The object's Distinguished Name. Same as the Data in the ObjectDN filter, if was used.")
    
class MutualPreviewValue_GroupResultsByOperation(BaseModel):
    value: bool = Field(description="Should the results be grouped by the Operation? Same as the Data in the GroupResultsByOperation filter, if was used.")
    
class MutualPreviewValue_sAMAccountName(BaseModel):
    value: str = Field(description="The user logon name, used for backwards compatibility with older versions of Windows. Same as the Data in the sAMAccountName filter, if was used.")
