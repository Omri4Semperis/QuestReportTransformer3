from typing import List, Literal, Optional, Union
from pydantic import BaseModel, Field

class LDAPFilteringNode(BaseModel):
    # TODO post processing to $type
    DollarType     : str                            = "Semperis.ReportTemplates.DataSource.Data.LDAPTreeNode, Semperis.ReportTemplates.DataSource.Data"
    # TODO is there a list of valid syntaxes?
    Syntax         : str                            = Field(description="The syntax of the LDAP attribute, e.g. 'DN', 'Oid', 'DirectoryString', etc.")
    Attribute      : str                            = Field(description="The LDAP attribute to filter on, e.g. 'objectCategory', 'objectClass', 'department', 'title', 'mail', 'userAccountControl', etc.")
    Alias          : Optional[str]                  = Field(Default=None, description="An optional alias for the attribute, can be None if not assigned.")
    # TODO is this Semperis specific? Is there a list of valid values and their meaning/logic?
    Data           : str                            = Field(description="The default value for the attribute filtration, e.g. 'user', 'Engineering', 'Senior Engineer', '*', 'Rel:1D', etc.")
    # TODO is there a list of valid syntaxe for UI?
    SyntaxUI       : str                            = Field(description="The UI representation of the syntax, e.g. 'String', 'SelectionFromList', 'SelectionFromFlags', 'CalculatedDateTime', etc.")
    DataInputMethod: Literal['UserInput', 'Preset'] = Field(description="The method of data input, either 'UserInput' or 'Preset'.")
    # TODO is there a list of valid values?
    Type           : str                            = Field(description="The type of operation to perform on the Attribute using the Data, e.g. 'Equal', 'Present', 'Extensible', 'LessThanOrEqualTo', 'GreaterThanOrEqualTo', etc.")
    # TODO is there a list of valid operations and their meaning/logic?
    Operation      : str                            = Field(description="The operation to perform, e.g. '=', '<=', '>='.")

class LDAPFilteringNotNode(BaseModel):
    # TODO post processing to $type
    DollarType: str                     = "Semperis.ReportTemplates.DataSource.Data.LDAPTreeNodeCondition, Semperis.ReportTemplates.DataSource.Data"
    Nodes     : List[LDAPFilteringNode] = Field(description="List containing a single LDAPFilteringNode to negate. You must include exactly one node in this list.")
    Type      : str                     = "Not"
    Operation : str                     = "!"

class LDAPInnerFilterSchema(BaseModel):
    # TODO post processing to $type
    DollarType: str                                                  = "Semperis.ReportTemplates.DataSource.Data.LDAPTreeNodeCondition, Semperis.ReportTemplates.DataSource.Data"
    Nodes     : List[Union[LDAPFilteringNode, LDAPFilteringNotNode]] = Field(description="List of LDAP nodes that define the filter conditions. Can contain LDAPFilteringNode and LDAPFilteringNotNode instances.")
    Type      : str                                                  = 'And'
    Operation : str                                                  = '&'

class LDAPFilterSchema(BaseModel):
    # TODO post processing to $type
    DollarType    : str                   = "Semperis.ReportTemplates.DataSource.Data.LDAPFilter.ADFilterQuery, Semperis.ReportTemplates.DataSource.Data"
    LDAPFilter    : LDAPInnerFilterSchema = Field(description="The filter field of the report, defining $type, Nodes, Type and Operation. It is an instance of LDAPInnerFilterSchema.")
    BaseDNs       : str                   = None
    SearchScope   : str                   = None
    ObjectListIds : str                   = None
    IsGC          : bool                  = None
    MaxResultLimit: int                   = 0