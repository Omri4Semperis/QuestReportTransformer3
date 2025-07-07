from pydantic import BaseModel, Field

"""# Filters available only for DNS reports
1. Zones: Active Directory DNS zones. Mandatory for DNS reports. Allowed states: This filter's only state is 'Include'. The input Can be 'Preset' or 'UserInput'. Allowed values: Closed list: The available Zones.
2. RecordTypes: DNS record types, defined in the DNS standards. Not mandatory. Allowed states: Can only be set to one of these: [Include, Exclude]. The input Can be 'Preset' or 'UserInput'. Allowed values: The ones still widely used today: A, NS, CNAME, SOA. May also include the historical ones."""

# TODO post process to a single value in a list

class MutualPreviewValue_Zones(BaseModel):
    value: str = Field(description="The Zones to consider. Same as the Data in the Zones filter, if was used.")

class MutualPreviewValue_RecordTypes(BaseModel):
    value: str = Field(description="The DNS record types to consider. Same as the Data in the RecordTypes filter, if was used.")