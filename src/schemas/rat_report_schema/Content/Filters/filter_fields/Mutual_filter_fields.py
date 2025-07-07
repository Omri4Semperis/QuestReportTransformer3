from typing import List, Literal, Set

from pydantic import BaseModel, Field

preset_userinput_explanation = "If Preset then a value (which is defined in PreviewValues field) is presented as a default and if UserInput then no default value is presented"

"""# Filters available for both DNS and NonDNS reports
1. Type:
        Determines if the report is DNS or NonDNS. Mandatory for both DNS and NonDNS.
        Allowed states: Only state is 'Is'.
        The input Can only be 'Preset'.
        Allowed values: DNS or NonDNS."""
"""
2. DateRange:
        The date range to consider. Not mandatory.                    
        Allowed states: Only state is 'Is'.
        The input Can be 'Preset' or 'UserInput'.
        Allowed values: Can be relative or absolute."""
"""
3. Operations:
        The types of AD operations. Not mandatory.                    
        Allowed states: Can only be set to one of these: [Include, Exclude].
        The input Can be 'Preset' or 'UserInput'.
        Allowed values: Multiple choice from: Create, Modify, Add, Remove, Move, Delete, Restore"""
"""
4. OldValue:
        The old value of the object's attribute. Not mandatory.                    
        Allowed states: Can only be set to one of these: [Contains, NotContain, Equals, NotEquals IsNotNullAndNotEmpty, IsNullOrEmpty].
        The input Can be 'Preset' or 'UserInput'.
        Allowed values: Free text."""
"""
5. NewValue:
        The new value of the object's attribute. Not mandatory.                    
        Allowed states: Can only be set to one of these: [Contains, NotContain, Equals, NotEquals IsNotNullAndNotEmpty, IsNullOrEmpty].
        The input Can be 'Preset' or 'UserInput'.
        Allowed values: Free text."""
"""
6. ChangedBy:
        The value of the object that caused the change. Not mandatory.                    
        Allowed states: Can only be set to one of these: [Contains, NotContain, Equals, NotEquals IsNotNullAndNotEmpty, IsNullOrEmpty].
        The input Can be 'Preset' or 'UserInput'.
        Allowed values: Free text."""
"""
7. SourceServers:
        Domain controllers or DNS servers that are the source of the data. Not mandatory.                    
        Allowed states: Can only be set to one of these: [Include, Exclude].
        The input Can be 'Preset' or 'UserInput'.
        Allowed values: Closed list: The available Source Servers."""
"""
8. ObjectListIds:
        internal identifiers or unique IDs. Not mandatory.                    
        Allowed states: Can only be set to one of these: [Equals, not equals, starts with, ends with].
        The input Can be 'Preset' or 'UserInput'.
        Allowed values: Free text."""

# Can be deprecated as it's defined manually for bot DNS and NonDNS reports
class MutualFilterField_Type(BaseModel):
    FieldName:       str                      = "Type"
    State:           str                      = "Is"
    DataInputMethod: str                      = "Preset"
    Data:            Literal["DNS", "NonDNS"] = Field(description="Determines if the report is DNS or NonDNS.")

class MutualFilterField_DateRange(BaseModel):
    FieldName:       str =                            "DateRange"
    State:           str =                            "Is"
    DataInputMethod: Literal["Preset", "UserInput"] = Field(description=preset_userinput_explanation)
    Data:            str =                            Field(description="The date range to consider. Can be relative (e.g. 'Rel:2M' for the last 2 months or 'Rel:1W' for the last week) or absolute (e.g. 'Abs:2025-06-02T07:16:56.9737401+00:00,2025-07-02T07:16:56.9737401+00:00')")
    
class MutualFilterField_Operations(BaseModel):
    FieldName:       str =                                                                            "Operations"
    State:           Literal["Include", "Exclude"] =                                                  Field(description="The types of AD operations")
    DataInputMethod: Literal["Preset", "UserInput"] =                                                 Field(description=preset_userinput_explanation)
    # TODO: Post processing from set of string into a single string of ';' separated words
    Data:            Set[Literal["Create", "Modify", "Add", "Remove", "Move", "Delete", "Restore"]] = Field(description="The operations to include or exclude. Multiple choice from: Create, Modify, Add, Remove, Move, Delete, Restore")
    
class MutualFilterField_OldValue(BaseModel):
    FieldName:       str =                                                                                               "OldValue"
    State:           Literal["Contains", "NotContain", "Equals", "NotEquals", "IsNotNullAndNotEmpty", "IsNullOrEmpty"] = Field(description="The relation of the data to the field.")
    DataInputMethod: Literal["Preset", "UserInput"] =                                                                    Field(description=preset_userinput_explanation)
    Data:            str =                                                                                               Field(description="The old value of the object's attribute.")
    
class MutualFilterField_NewValue(BaseModel):
    FieldName:       str =                                                                                               "NewValue"
    State:           Literal["Contains", "NotContain", "Equals", "NotEquals", "IsNotNullAndNotEmpty", "IsNullOrEmpty"] = Field(description="The relation of the data to the field.")
    DataInputMethod: Literal["Preset", "UserInput"] =                                                                    Field(description=preset_userinput_explanation)
    Data:            str =                                                                                               Field(description="The new value of the object's attribute.")
    
class MutualFilterField_ChangedBy(BaseModel):
    FieldName:       str =                                                                                              "ChangedBy"
    State:           Literal["Contains", "NotContain", "Equals", "NotEquals", "IsNotNullAndNotEmpty", "IsNullOrEmpty"] = Field(description="The relation of the data to the field.")
    DataInputMethod: Literal["Preset", "UserInput"] =                                                                    Field(description=preset_userinput_explanation)
    # TODO make sure I got it right
    Data:            str =                                                                                               Field(description="The value of the object that caused the change.")
    
class MutualFilterField_SourceServers(BaseModel):
    FieldName:       str =                            "SourceServers"
    State:           Literal["Include", "Exclude"] =  Field(description="The relation of the data to the field.")
    DataInputMethod: Literal["Preset", "UserInput"] = Field(description=preset_userinput_explanation)
    # TODO: Post processing from set of string into a single string of ';' separated words
    Data:            Set[str] =                       Field(description="Domain controllers or DNS servers that are the source of the data. Closed list: The available Source Servers.")
    
class MutualFilterField_ObjectListIds(BaseModel):
    FieldName:       str =                                                      "ObjectListIds"
    State:           Literal["Equals", "NotEquals", "StartsWith", "EndsWith"] = Field(description="The relation of the data to the field.")
    DataInputMethod: Literal["Preset", "UserInput"] =                           Field(description=preset_userinput_explanation)
    # TODO make sure I got it right
    Data:            str =                                                      Field(description="Internal identifiers or unique IDs. Free text.")