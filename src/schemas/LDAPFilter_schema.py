from typing import List, Literal, Optional, Union
from pydantic import BaseModel, Field

LDAPFilteringNode_dollar_type_value           = "Semperis.ReportTemplates.DataSource.Data.LDAPTreeNode, Semperis.ReportTemplates.DataSource.Data"
LDAPFilteringNode_Syntax_description          = "The syntax of the LDAP attribute, e.g. 'DN', 'Oid', 'DirectoryString', etc."  # TODO is there a list of valid syntaxes?
LDAPFilteringNode_Attribute_description       = "The LDAP attribute to filter on, e.g. 'objectCategory', 'objectClass', 'department', 'title', 'mail', 'userAccountControl', etc."
LDAPFilteringNode_Alias_description           = "An optional alias for the attribute, can be None if not assigned."
LDAPFilteringNode_Data_description            = "The default value for the attribute filtration, e.g. 'user', 'Engineering', 'Senior Engineer', '*', 'Rel:1D', etc." # TODO is this Semperis specific? Is there a list of valid values and their meaning/logic?
LDAPFilteringNode_SyntaxUI_description        = "The UI representation of the syntax, e.g. 'String', 'SelectionFromList', 'SelectionFromFlags', 'CalculatedDateTime', etc." # TODO is there a list of valid syntaxe for UI?
LDAPFilteringNode_DataInputMethod_description = "The method of data input, either 'UserInput' or 'Preset'."
LDAPFilteringNode_Type_description            = "The type of operation to perform on the Attribute using the Data, e.g. 'Equal', 'Present', 'Extensible', 'LessThanOrEqualTo', 'GreaterThanOrEqualTo', etc."  # TODO is there a list of valid values?
LDAPFilteringNode_Operation_description       = "The operation to perform, e.g. '=', '<=', '>='."  # TODO is there a list of valid operations and their meaning/logic?

class LDAPFilteringNode(BaseModel):
    """
    "$type"          : (str) Always 'Semperis.ReportTemplates.DataSource.Data.LDAPTreeNode,
                                     Semperis.ReportTemplates.DataSource.Data',
	"Syntax"         : (str) e.g. 'DN'; 'Oid'; 'DirectoryString'; 'Int'; 'GeneralizedTime' etc,
	"Attribute"      : (str) e.g. 'objectCategory'; 'objectClass'; 'department'; 'title'; 'mail'; 'userAccountControl';
                                  'physicalDeliveryOfficeName'; 'whenCreated'; etc.,
	"Alias"          : (str, nullable) The alias the user wants to give to this attribute; Null if no alias assigned,
	"Data"           : (str) defualt value for the attribute filtration; e.g. 'user'; 'Engineering'; 'Senior Engineer';
                                                                              '*'; 'Rel:1D'; ;,
	"SyntaxUI"       : (str) e.g. 'String'; 'SelectionFromList'; 'SelectionFromFlags'; 'CalculatedDateTime' etc.,
	"DataInputMethod": (str) 'UserInput' or 'Preset',
	"Type"           : (str) e.g. 'Equal'; 'Present'; 'Extensible'; 'LessThanOrEqualTo'; 'GreaterThanOrEqualTo' etc.,
	"Operation"      : (str) e.g. '='; '<='; '>='
    """
    DollarType     : str                            = LDAPFilteringNode_dollar_type_value  # $type
    Syntax         : str                            = Field(description=LDAPFilteringNode_Syntax_description)
    Attribute      : str                            = Field(description=LDAPFilteringNode_Attribute_description)
    Alias          : Optional[str]                  = Field(Default=None, description=LDAPFilteringNode_Alias_description)
    Data           : str                            = Field(description=LDAPFilteringNode_Data_description)
    SyntaxUI       : str                            = Field(description=LDAPFilteringNode_SyntaxUI_description)
    DataInputMethod: Literal['UserInput', 'Preset'] = Field(description=LDAPFilteringNode_DataInputMethod_description)
    Type           : str                            = Field(description=LDAPFilteringNode_Type_description)
    Operation      : str                            = Field(description=LDAPFilteringNode_Operation_description)

LDAPFilteringNotNode_dollar_type_value = "Semperis.ReportTemplates.DataSource.Data.LDAPTreeNodeCondition, Semperis.ReportTemplates.DataSource.Data"
LDAPFilteringNotNode_Nodes_description = "List containing a single LDAPFilteringNode to negate. You must include exactly one node in this list."

class LDAPFilteringNotNode(BaseModel):
    """
	"$type": (str) 'Semperis.ReportTemplates.DataSource.Data.LDAPTreeNodeCondition,
                    Semperis.ReportTemplates.DataSource.Data',
	"Nodes": List always with a single Node to negate [LDAPFilteringNode],
	"Type": Always 'Not',
	"Operation": "!"
    """
    DollarType: str                     = LDAPFilteringNotNode_dollar_type_value  # $type
    Nodes     : List[LDAPFilteringNode] = Field(description=LDAPFilteringNotNode_Nodes_description)
    Type      : str                     = "Not"
    Operation : str                     = "!"


LDAPInnerFilterSchema_dollar_type_value = "Semperis.ReportTemplates.DataSource.Data.LDAPTreeNodeCondition, Semperis.ReportTemplates.DataSource.Data"
LDAPInnerFilterSchema_nodes_description = "List of LDAP nodes that define the filter conditions. Can contain LDAPFilteringNode and LDAPFilteringNotNode instances."

class LDAPInnerFilterSchema(BaseModel):
    """Schema for the LDAP filter nodes in RAT reports."""
    DollarType: str                                                  = LDAPInnerFilterSchema_dollar_type_value  # $type
    Nodes     : List[Union[LDAPFilteringNode, LDAPFilteringNotNode]] = Field(description=LDAPInnerFilterSchema_nodes_description)
    Type      : str                                                  = 'And'
    Operation : str                                                  = '&'

LDAPFilterSchema_dollar_type_value = "Semperis.ReportTemplates.DataSource.Data.LDAPFilter.ADFilterQuery, Semperis.ReportTemplates.DataSource.Data"
LDAPFilterSchema_LDAPFilter_description = "The filter field of the report, defining $type, Nodes, Type and Operation. It is an instance of LDAPInnerFilterSchema."

class LDAPFilterSchema(BaseModel):
    """Schema for the Content/Filter fields of RAT reports.
    
    "Filter" (Maps to a dict in which all keys are mandatory,
              some of their values are nullable as per details listed here): (dict) {
        "$type": (literal str) always 'Semperis.ReportTemplates.DataSource.Data.LDAPFilter.ADFilterQuery,
                                       Semperis.ReportTemplates.DataSource.Data',
        "LDAPFilter": (LDAPInnerFilterSchema),
        "BaseDNs": Always null,
        "SearchScope": Always null,
        "IsGC": Always null,
        "MaxResultLimit": (literal int) Always 0,
        "ObjectListIds": Always null
    },
    """    
    DollarType    : str                   = LDAPFilterSchema_dollar_type_value # $type
    LDAPFilter    : LDAPInnerFilterSchema = Field(description=LDAPFilterSchema_LDAPFilter_description)
    BaseDNs       : str                   = None
    SearchScope   : str                   = None
    ObjectListIds : str                   = None
    IsGC          : bool                  = None
    MaxResultLimit: int                   = 0