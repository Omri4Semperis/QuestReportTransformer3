from typing import List, Literal, Set

from pydantic import BaseModel, Field

preset_userinput_explanation = "If Preset then a value (which is defined in PreviewValues field) is presented as a default and if UserInput then no default value is presented"

"""# Filters available only for NonDNS reports
1. Partitions:
        Active Directory DNS partitions.
        Mandatory for NonDNS reports.
        Allowed states: Can only be set to one of these: [Include, Exclude].
        The input Can be 'Preset' or 'UserInput'.
        Allowed values: Closed list: The available Partitions."""
"""
2. ObjectClasses:
        The AD object classes. Not Mandatory.
        Allowed states: Can only be set to one of these: [Include, Exclude].
        The input Can be 'Preset' or 'UserInput'.
        Allowed values: Multiple choice from all Active Directory object classes (e.g. aCSresourceLimits, applicationSettings, account, aCSPolicy...)"""
"""
3. Attributes:
        The AD attributes. Not Mandatory. 
        Allowed states: Can only be set to one of these: [Include, Exclude].
        The input Can be 'Preset' or 'UserInput'.
        Allowed values: Multiple choice from all Active Directory attribute names (e.g. accountNameHistory, accountExpires, aCSAggregateTokenRatePerUser…)"""
"""
4. ObjectDN:
        The object's Distinguished Name. Not Mandatory.
        Allowed states: Can only be set to one of these: [Equals, not equals, starts with].
        The input Can be 'Preset' or 'UserInput'.
        Allowed values: Domain id."""
"""
5. GroupResultsByOperation:
        Determines if the results should be grouped by the Operation type. Not Mandatory.
        Allowed states: Only state is 'Is'.
        The input Can be 'Preset' or 'UserInput'.
        Allowed values: true or false."""
"""
6. sAMAccountName:
        The user logon name, used for backwards compatibility with older versions of Windows. Not Mandatory.
        Allowed states: Can only be set to one of these: [Equals, not equals, starts with, ends with].
        The input Can be 'Preset' or 'UserInput'.
        Allowed values: Free text."""

class NonDNSFilterField_Partitions(BaseModel):
    FieldName:       str =                            "Partitions"
    State:           Literal["Include", "Exclude"] =  Field(description="Whether to include or exclude the Active Directory partitions.")
    DataInputMethod: Literal["Preset", "UserInput"] = Field(description=preset_userinput_explanation)
    Data:            List[str] =                      Field(description="A closed list of the available Partitions. E.g. 'CN=Configuration,DC=d01,DC=lab'")
    
class NonDNSFilterField_ObjectClasses(BaseModel):
    FieldName:       str =                            "ObjectClasses"
    State:           Literal["Include", "Exclude"] =  Field(description="Whether to include or exclude the AD object classes.")
    DataInputMethod: Literal["Preset", "UserInput"] = Field(description=preset_userinput_explanation)
    # TODO Post processing: from set of string into a single string of ';' separated words
    Data:            Set[str] =                       Field(description="Multiple choice from all Active Directory object classes (e.g. aCSresourceLimits, applicationSettings, account, aCSPolicy...)")
    
class NonDNSFilterField_Attributes(BaseModel):
    FieldName:       str =                            "Attributes"
    State:           Literal["Include", "Exclude"] =  Field(description="Whether to include or exclude the AD attributes.")
    DataInputMethod: Literal["Preset", "UserInput"] = Field(description=preset_userinput_explanation)
    # TODO Post processing: from set of string into a single string of ';' separated words
    Data:            Set[str] =                       Field(description="Multiple choice from all Active Directory attribute names (e.g. accountNameHistory, accountExpires, aCSAggregateTokenRatePerUser…)")

class NonDNSFilterField_ObjectDN(BaseModel):
    FieldName:       str =                                          "ObjectDN"
    State:           Literal["Equals", "NotEquals", "StartsWith"] = Field(description="The relation of the ObjectDN data to the field.")
    DataInputMethod: Literal["Preset", "UserInput"] =               Field(description=preset_userinput_explanation)
    Data:            str =                                          Field(description="The object's Distinguished Name, domain id.")

class NonDNSFilterField_GroupResultsByOperation(BaseModel):
    FieldName:       str =                            "GroupResultsByOperation"
    State:           str =                            "Is"
    DataInputMethod: Literal["Preset", "UserInput"] = Field(description=preset_userinput_explanation)
    Data:            bool =                           Field(description="Determines if the results should be grouped by the Operation type.")

class NonDNSFilterField_sAMAccountName(BaseModel):
    FieldName:       str =                                                      "sAMAccountName"
    State:           Literal["Equals", "NotEquals", "StartsWith", "EndsWith"] = Field(description="The relation of the sAMAccountName data to the field.")
    DataInputMethod: Literal["Preset", "UserInput"] =                           Field(description=preset_userinput_explanation)
    Data:            str =                                                      Field(description="The user logon name, used for backwards compatibility with older versions of Windows.")