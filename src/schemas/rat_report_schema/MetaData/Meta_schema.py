from typing import Literal, Optional
from pydantic import BaseModel, Field

timestamp_format = "YYYY-MM-DDTHH:MM:SS.sssZ"

def generate_random_unique_id() -> str:
    """Generates a random unique ID using UUID4.
    
    Returns:
        A random unique ID as a string."""
    import uuid
    return str(uuid.uuid4())

class CategoryIDException(Exception):
    """Custom exception for invalid category ID names."""
    def __init__(self, message: str):
        super().__init__(message)
        

def category_id_from_name(
    name: Literal["General", "Operational", "Best Practices", "Service Accounts", "Regulatory Compliance", "Security"]
    ) -> Literal["9f506583-d530-4c66-a9a7-322429d828ef",
            "b6b8b0f5-2072-48ba-958e-4999353277fd",
            "76512d4d-43ea-4b29-92cc-5914e67cf13a",
            "b6a65ae0-78df-4ee0-a91e-e30a8da1da20",
            "55d2774f-3def-41c6-a93f-f07c6d2f29e5",
            "8b8a7eed-c190-42f4-88aa-fc47f85532e6"]:
    """
    Returns the category ID based on the given category name.
    Valid names are: "General", "Operational", "Best Practices", "Service Accounts", "Regulatory Compliance", "Security".
    
    Args:
        name (Literal): The name of the category.
    Returns:
        str: The category ID corresponding to the given name.
    Raises:
        CategoryIDException: If the name is not valid.
    """
    categories = {"General": "9f506583-d530-4c66-a9a7-322429d828ef",
        "Operational": "b6b8b0f5-2072-48ba-958e-4999353277fd",
        "Best Practices": "76512d4d-43ea-4b29-92cc-5914e67cf13a",
        "Service Accounts": "b6a65ae0-78df-4ee0-a91e-e30a8da1da20",
        "Regulatory Compliance": "55d2774f-3def-41c6-a93f-f07c6d2f29e5",
        "Security": "8b8a7eed-c190-42f4-88aa-fc47f85532e6"}
    
    if name not in categories:
        raise CategoryIDException(f"Invalid category name: {name}. Valid names are: {', '.join(categories.keys())}")
    
    return categories[name]

class MetaDataSchema(BaseModel):
    CategoryId    : Literal["General", "Operational", "Best Practices", "Service Accounts", "Regulatory Compliance", "Security"] = Field(..., description="Report category")
    ReportType    : Literal["ADTemplate", "DBTemplate"] = Field(..., description="'ADTemplate' for LDAP reports and 'DBTemplate' for DB reports")
    # TODO find out the logic behind LicenseLevel and confirm its correctness in post-processing
    LicenseLevel  : Literal['None'] = Field(..., default='None', description="You MUST include this field and set it to string 'None'.")
    IndicatorTypes: Optional[str] = Field(..., description="MUST be privided, value is a always a native None")
    Targets       : Optional[str] = Field(..., description="MUST be privided, value is a always a native None")
    # TODO post-process to make sure this is a valid UUID4
    UniqueId      : str = Field(..., description="Always wirte: 'This will be done in post-processing step'. ")
    Name          : str = Field(..., description="Report name. Give this report a meaningful name, concisely describing its purpose.")
    # TODO find out the logic behind MinVerDsp and confirm its correctness in post-processing
    MinVerDsp     : float = Field(..., description="One of the following: 3.0, 3.8, 4.0, 4.1, 5.0")    
    Version       : int = Field(..., default=0, description="This field is mandatory and should be set to 0, unless explicitly asked for something else by the user.")
    # TODO find out logic behind the Company field and confirm its correctness in post-processing
    Company       : Literal["Semperis", "LDC"] = Field(..., description="Company name, usually Semperis")
    Description   : str = Field(..., description="Descrition of the reports purpose, actions it performs, and any other relevant information- all in a structured way. E.g. 'Purpose: ...\nLogic: In order to <>, we can filter by <>...\nFilters: ...\nDisplays used: ...\nNotes: ...'")
    # TODO find out logic behind the IsSecurity field and confirm its correctness in post-processing
    IsSecurity    : bool = Field(..., default=False, description="This field is mandatory and should be set to False.")
    # TODO find out logic behind the Status field and confirm its correctness in post-processing
    Status        : str = Field(..., default='internal', description="This field is mandatory and should be set to 'internal'.")
    CreatedAt     : str = Field(..., description=f"A timestamp of format {timestamp_format}")
    ImportedAt    : str = Field(..., description=f"A timestamp of format {timestamp_format}")
    ModifiedAt    : str = Field(..., description=f"A timestamp of format {timestamp_format}")
    # TODO find out logic behind the Weight field and confirm its correctness in post-processing
    Weight        : int = Field(..., default=1, description="This field is mandatory and should be set to 1.")