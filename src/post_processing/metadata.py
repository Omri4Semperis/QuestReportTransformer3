from typing import Dict, Optional, Union
from src.schemas.rat_report_schema.MetaData.Meta_schema import category_id_from_name, generate_random_unique_id


def fix_category_id(metadata: Dict[str, Optional[Union[str, float, int]]]) -> Dict[str, Optional[Union[str, float, int]]]:
    category_name = metadata.get("CategoryId")
    if category_name is None:
        metadata["CategoryId"] = "General"
    category_id = category_id_from_name(category_name)
    metadata["CategoryId"] = category_id
    
    return metadata

def fix_unique_ids(metadata: Dict[str, Optional[Union[str, float, int]]]) -> Dict[str, Optional[Union[str, float, int]]]:
    new_unique_id = generate_random_unique_id()
    metadata["UniqueId"] = new_unique_id
    
    return metadata

def post_process_metadata(metadata: Dict[str, Optional[Union[str, float, int]]]) -> Dict[str, Optional[Union[str, float, int]]]:
    """
    Post-process the metadata by adding or modifying fields as necessary.
    """
    # Example modification: Set a default value for a field if not provided
    meta_data = fix_category_id(metadata)
    meta_data = fix_unique_ids(meta_data)
    
    return metadata