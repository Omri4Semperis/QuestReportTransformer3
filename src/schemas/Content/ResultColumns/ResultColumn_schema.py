from typing import Dict, Literal, Optional, Union, List
from pydantic import BaseModel, Field

SelectedFormatterSchema_DollarType_description:str = "The formatter type of this field"
SelectedFormatterSchema_Name_description      :str = "Specific formatters per field. See list below to know which formatter goes with which field"

class SelectedFormatterSchema(BaseModel):
    """
    It represents a specific formatter for a column in the report's output.
    Schema (All fields are mandatory):
    {
        "$type": Literal[] The formatter type,
        "Name": (str) specific formatters per field. See list below to know which formatter goes with which field
    }
    """
    DollarType: Literal[
        "Semperis.ReportTemplates.DataSource.DB.ADSyntaxFormatter, Semperis.ReportTemplates.DataSource.DB",  # For From_Syntax, To_Syntax
        "Semperis.ReportTemplates.DataSource.DB.DBDateTimeFormatter, Semperis.ReportTemplates.DataSource.DB", # For CollectionTime, OriginatingTime, Valid Until, ValidUntil
        "Semperis.ReportTemplates.DataSource.Data.DefaultFormatter, Semperis.ReportTemplates.DataSource.Data"  # For all other fields
        ] = Field(description=SelectedFormatterSchema_DollarType_description)
    Name: Literal[
        "ADSyntax Formatting",  # For From_Syntax, To_Syntax
        "Universal sortable date/time pattern",  # For CollectionTime, OriginatingTime, Valid Until, ValidUntil
        "No Formatting"  # For all other fields
        ] = Field(description=SelectedFormatterSchema_Name_description)

ResultColumnSchema_DollarType_value             : str = "Semperis.ReportTemplates.DataSource.DB.DBDataColumn, Semperis.ReportTemplates.DataSource.DB"
ResultColumnSchema_Name_description             : str = "The name of the column/field. e.g. 'from_stringvalue'; 'from_syntax'; 'modificationtype'; 'originatinguserworkstations';"
ResultColumnSchema_Alias_description            : str = "An alias the user wants to assign the column instead of the real name"
ResultColumnSchema_SelectedFormatter_description: str = "The formatter to use for this column"

class ResultColumnSchema(BaseModel):
    """
    A ResultColumn is Dict[str, Union[str, Dict[str, str]]] object. It represents a single column which will be displayed in the report's output. A list of ResultColumn is mapped to by Content/ResultColumns.
    Schema (All fields are mandatory, some are nullable):
    {
        "$type"            : (str) Always 'Semperis.ReportTemplates.DataSource.DB.DBDataColumn, Semperis.ReportTemplates.DataSource.DB',
        "Name"             : (str) The name of the column/field. e.g. 'from_stringvalue'; 'from_syntax'; 'modificationtype'; 'originatinguserworkstations';,
        "Alias"            : (str, nullable) An alias the user wants to assign the column instead of the real name,
        "SelectedFormatter": {
            "$type": (str) Always 'Semperis.ReportTemplates.DataSource.DB.DBDateTimeFormatter, Semperis.ReportTemplates.DataSource.DB',
            "Name": (str) specific formetters per field. See list bellow to know which formatter goes with which filed
        }
    }
    """
    DollarType       : str                     = ResultColumnSchema_DollarType_value
    Name             : str                     = Field(description=ResultColumnSchema_Name_description)  # TODO need to find a smart way to assert that DNS and NonDNS get their respective options for columns names
    Alias            : Optional[str]           = Field(default=None, description=ResultColumnSchema_Alias_description)
    SelectedFormatter: SelectedFormatterSchema = Field(description=ResultColumnSchema_SelectedFormatter_description)