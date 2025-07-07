from typing import List, Literal, Set

from pydantic import BaseModel, Field

preset_userinput_explanation = "If Preset then a value (which is defined in PreviewValues field) is presented as a default and if UserInput then no default value is presented"

"""# Filters available only for DNS reports
1. Zones:
        Active Directory DNS zones. Mandatory for DNS reports.
        Allowed states: This filter's only state is 'Include'.
        The input Can be 'Preset' or 'UserInput'.
        Allowed values: Closed list: The available Zones."""
"""
2. RecordTypes:
        DNS record types, defined in the DNS standards. Not mandatory.
        Allowed states: Can only be set to one of these: [Include, Exclude].
        The input Can be 'Preset' or 'UserInput'.
        Allowed values: The ones still widely used today: A, NS, CNAME, SOA. May also include the historical ones."""

class DNSFilterField_Zones(BaseModel):
    FieldName:       str =                            "Zones"
    State:           str =                            "Include"
    DataInputMethod: Literal["Preset", "UserInput"] = Field(description=preset_userinput_explanation)
    # TODO find out if this list is taken from somewhere, if it can be fetched or inferred somehow.
    # TODO Post processing: from set of string into a single string of ';' separated words
    Data:            Set[str] =                       Field(description="A closed list of the available Zones. E.g. ..TrustAnchors (DC=ForestDnsZones,DC=d01,DC=lab), _msdcs.d01.lab (DC=ForestDnsZones,DC=d01,DC=lab), d01.lab (DC=DomainDnsZones,DC=d01,DC=lab), etc.")
    
class DNSFilterField_RecordTypes(BaseModel):
    FieldName:       str =                            "RecordTypes"
    State:           Literal["Include", "Exclude"] =  Field(description="Whether to include or exclude the DNS record types, defined in the DNS standards.")
    DataInputMethod: Literal["Preset", "UserInput"] = Field(description=preset_userinput_explanation)
    # TODO Post processing: from set of string into a single string of ';' separated words
    Data:            Set[str] =                       Field(description="Can be any of 'ZERO, A, NS, ..., ZONE' but the most common ones are: A, NS, CNAME, SOA. May also include the historical ones.")