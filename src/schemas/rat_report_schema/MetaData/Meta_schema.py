from typing import Literal
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

class MetaSchema(BaseModel):
    """Schema for the metadata fields of RAT reports."""
    
    Name           : str = Field(description="Report name")
    Description    : str = Field(description="Descrition of the report")
    UniqueId       : str = Field(description="A randomized unique uuid4")
    CreatedAt      : str = Field(description=f"A timestamp of format {timestamp_format}")
    ImportedAt     : str = Field(description=f"A timestamp of format {timestamp_format}")
    ModifiedAt     : str = Field(description=f"A timestamp of format {timestamp_format}")
    MinVerDsp      : float = Field(description="One of the following: 3.0, 3.8, 4.0, 4.1, 5.0")
    Company        : Literal["Semperis", "LDC"] = Field(description="Company name, Usually Semperis")
    CategoryId     : Literal["General", "Operational", "Best Practices", "Service Accounts", "Regulatory Compliance", "Security"] = Field(description="Report category")
    ReportType     : Literal["ADTemplate", "DBTemplate"] = Field(description="'ADTemplate' for LDAP reports and 'DBTemplate' for DB reports")
    Status         : str = 'internal'
    LicenseLevel   : str = 'None'
    IndicatorTypes : str = None
    Targets        : str = None
    Version        : int = 0
    Weight         : int = 1
    IsSecurity     : bool = False