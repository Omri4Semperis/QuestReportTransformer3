from typing import Dict, Optional, Union
from src.schemas.rat_report_schema.MetaData.Meta_schema import category_id_from_name, generate_random_unique_id, timestamp_format
import datetime

def fix_category_id(metadata: Dict[str, Optional[Union[str, float, int]]]) -> Dict[str, Optional[Union[str, float, int]]]:
    category_name = metadata.get("CategoryId")
    if category_name is None:
        metadata["CategoryId"] = "General"
    category_id = category_id_from_name(category_name)
    metadata["CategoryId"] = category_id
    
    return metadata

def set_unique_ids(metadata: Dict[str, Optional[Union[str, float, int]]]) -> Dict[str, Optional[Union[str, float, int]]]:
    new_unique_id = generate_random_unique_id()
    metadata["UniqueId"] = new_unique_id
    
    return metadata

def set_times(metadata: Dict[str, Optional[Union[str, float, int]]]) -> Dict[str, Optional[Union[str, float, int]]]:
    current_time = datetime.datetime.now().strftime(timestamp_format)
    metadata["CreatedAt"] = current_time
    metadata["ImportedAt"] = current_time
    metadata["ModifiedAt"] = current_time

    return metadata

def set_report_type(metadata: Dict[str, Optional[Union[str, float, int]]], report_type: str) -> Dict[str, Optional[Union[str, float, int]]]:
    metadata["ReportType"] = report_type
    return metadata

def post_process_metadata(
    meta_data_original: Dict[str, Optional[Union[str, float, int]]],
    report_type: str
) -> Dict[str, Optional[Union[str, float, int]]]:
    """
    Post-process the metadata by adding or modifying fields as necessary.
    """
    # Example modification: Set a default value for a field if not provided
    meta_data = meta_data_original.copy()
    meta_data = fix_category_id(meta_data_original)
    meta_data = set_unique_ids(meta_data)
    meta_data = set_times(meta_data)
    meta_data = set_report_type(meta_data, report_type)
    
    return meta_data