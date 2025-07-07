from typing import Dict, Literal, Optional, Union
from pydantic import BaseModel, Field


class LDAPPreviewValuesSchema(BaseModel):
    # TODO is there any governing logic independent of environment (which means we can further specify here)
    BaseDn: list[str] = Field(description="List of Base DNs, e.g. 'C=example,DC=com' or 'DC=hello' or 'OU=Blah'")
    # TODO Note: This value will have to be post-procssesed to be a single item in a list, i.e. ["0"] or ["1"] or ["2"]
    SearchScope: Literal["0", "1", "2"] = Field(description="List containing one single string: ['0'] = Base; ['1'] = One Level; ['2'] = Sub tree;")
    # TODO Note: This value will have to be post-processed to be a single item in a list, i.e. [True] or [False]
    IsGC: bool = Field(description="True if this report searches global catalog, False otherwise")
    # TODO Note: This value will have to be post-processed to be a list of strings of the form "<field>;<value>", e.g. ["objectClass;sitesContainer", "objectCategory;blah"] or ["objectClass;user", "whenCreated;Abs:2024-01-01T00:00:00.0000000", "whenCreated;Rel:1W"]
    TreeValues: Dict[str, str] = Field(description="A dictionary from the LDAP field to the value it is compared against. e.g. \{'objectClass': 'sitesContainer', 'objectCategory': 'blah'\}")
