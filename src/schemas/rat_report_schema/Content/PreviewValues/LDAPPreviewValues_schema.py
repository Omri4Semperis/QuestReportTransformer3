from typing import Dict, Literal, Optional, Union
from pydantic import BaseModel, Field

LDAPPreviewValuesSchema_BaseDn_description = (
    "List of Base DNs, e.g. 'C=example,DC=com' or 'DC=hello' or 'OU=Blah'"
)
LDAPPreviewValuesSchema_SearchScope_description = "List containing one single string: ['0'] = Base; ['1'] = One Level; ['2'] = Sub tree;"
LDAPPreviewValuesSchema_IsGC_description = (
    "True if this report searches global catalog, False otherwise"
)
LDAPPreviewValuesSchema_TreeValues_description = "A dictionary from the LDAP field to the value it is compared against. e.g. \{'objectClass': 'sitesContainer', 'objectCategory': 'blah'\}"


class LDAPPreviewValuesSchema(BaseModel):
    """
    Schema:
    "PreviewValues" (maps to a dict where all fields are mandatory and non nullable): (dict) {
        "BaseDn"     : (List[str]) for example 'C=example,DC=com' or 'DC=hello' or 'OU=Blah',
        "SearchScope": (List containing one single string: 0, 1 or 2) ['0'] = Base; ['1'] = One Level; ['2'] = Sub tree;,
        "IsGC"       : (List containing one single bool object) [True] if Search Global Catalog, [Flase] othersie,
        "TreeValues" : (List[str]) each string in the list has the form '<field>;<value>' where field and value are derived from the LDAP query. Example 1: if the query was (&(objectClass=user)(objectCategory=person)) then this value will be ["objectClass;sitesContainer", "objectCategory;blah"]. Example 2: for query (&(objectClass=user)(memberOf=CN=ProjectX-Team,OU=Groups,DC=example,DC=com)(telephoneNumber=*)(whenCreated>=20240101000000.0Z)) the value will be ["objectClass;subnet", "memberOf;CN=ProjectX-Team,OU=Groups,DC=example,DC=com", "telephoneNumber;*", "whenCreated;Rel:1D"]. Another example: ["objectClass;user", "whenCreated;Abs:2024-01-01T00:00:00.0000000", "whenCreated;Rel:1W"]
    },
    """

    BaseDn: list[str] = Field(
        description=LDAPPreviewValuesSchema_BaseDn_description
    )  # TODO is there any governing logic independent of environment (which means we can further specify here)
    SearchScope: Literal["0", "1", "2"] = Field(
        description=LDAPPreviewValuesSchema_SearchScope_description
    )  # TODO Note: This value will have to be post-procssesed to be a single item in a list, i.e. ["0"] or ["1"] or ["2"]
    IsGC: bool = Field(
        description=LDAPPreviewValuesSchema_IsGC_description
    )  # TODO Note: This value will have to be post-processed to be a single item in a list, i.e. [True] or [False]
    TreeValues: Dict[str, str] = Field(
        description=LDAPPreviewValuesSchema_TreeValues_description
    )  # TODO Note: This value will have to be post-processed to be a list of strings of the form "<field>;<value>", e.g. ["objectClass;sitesContainer", "objectCategory;blah"] or ["objectClass;user", "whenCreated;Abs:2024-01-01T00:00:00.0000000", "whenCreated;Rel:1W"]
