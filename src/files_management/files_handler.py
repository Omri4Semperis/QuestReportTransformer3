import datetime
import json
import os
import tkinter as tk
from tkinter import filedialog
from typing import Optional, Set, Tuple
import pandas as pd
from dataclasses import dataclass

from src.utils.azure_client_utils import ask


@dataclass
class ProcessedXMLFile:
    """Data class to hold information about a processed XML file."""
    filename: str
    original_content: str
    content_with_event_names: str
    events_found: Set[str]
    extracted_data: str
    subdir_name: str = ""


def get_artifacts_dir(exists_ok: bool = True) -> str:
    """
    Returns the path to the artifacts directory.
    Args:
        exists_ok (bool): If True, the function will not raise an error if the directory already exists.
                          If False, it will raise a FileExistsError if the directory already exists.
    Returns:
        str: The path to the artifacts directory with a timestamp.
    Raises:
        FileExistsError: If the directory already exists and exists_ok is False.
    """
    # Get current timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    dir_name = f"artifacts_{timestamp}"

    artifacts_dir = "artifacts"

    dir_path = os.path.join(os.getcwd(), artifacts_dir, dir_name)

    if not os.path.exists(dir_path):
        os.makedirs(dir_path, exist_ok=exists_ok)
    else:
        if not exists_ok:
            raise FileExistsError(f"Directory {dir_path} already exists.")
    return dir_path


def replace_event_ids_with_names(xml_content: str) -> Tuple[str, Set[str]]:
    """Replace event IDs with names in XML content."""
    res = xml_content
    df = pd.read_csv("knowledge/events_ids_names_mapping.csv")
    mapping = pd.Series(
        df["EventClassNames"].values,
        index=df["EventClassIDs"]).to_dict()

    events_found: Set[str] = set()

    # Replace event IDs with names in the XML content
    for event_id, event_name in mapping.items():
        res = res.replace(f'"{event_id}"', f'"{event_name}"')
        events_found.add(event_name)

    return res, events_found


def extract_data_about_report(content_with_event_names_instead_of_ids: str, events_found: Set[str]) -> str:
    """
    Extracts data about the report from the XML content.
    Args:
        content_with_event_names_instead_of_ids (str): The XML content with event names instead of IDs.
        events_found (Set[str]): A set of event names found in the content.
    """
    prompt = f"""Here's an XML report template content:
    <xml report template>
    {content_with_event_names_instead_of_ids}
    </xml report template>
    
    I think that it includes the following events:
    {events_found}
    
    Please tell me, in an elaborate way, what is the report about:
    - which environemt/scope does it search in?
    - Which events are included in the report?
    - Is there a daterange?
    - Other filtering parameters?
    - What information is displayed about the result? Which object fields?
    - Any other relevant information that you can extract from the XML content.
    
    Your summary will be used as a replacement for the report- so it should be inclusive, exhaustive and ellaborate.
    Start your answer with "# Report Overview and Extracted Data".
    """
    
    extracted_data_as_str = ask(
        system_prompt="You are a helpful assistant, expert at report understanding and data & insights extraction.",
        prompt=prompt)
    
    return extracted_data_as_str
    

def select_xml_file() -> Optional[str]:
    """
    Opens a file dialog to select an XML file.
    Returns:
        Optional[str]: The selected file path, or None if no file was selected.
    """
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    file_path = filedialog.askopenfilename(
        title="Select an XML file",
        filetypes=[("XML files", "*.xml"), ("All files", "*.*")],
    )
    
    print(f'{file_path=}')
    return file_path if file_path else None


def copy_and_read_xml_file(file_path: str, copy_to: Optional[str] = None) -> Tuple[str, str]:
    """
    Copies an XML file to a destination and reads its content.
    Args:
        file_path (str): Path to the XML file to read
        copy_to (Optional[str]): Directory to copy the file to
    Returns:
        Tuple[str, str]: (filename, content)
    """
    if copy_to:
        # Copy the file to the specified directory
        filename = os.path.basename(file_path)
        destination_path = os.path.join(copy_to, filename)

        # Read and write in text mode with the same encoding
        with open(file_path, "r", encoding="utf-16") as source_file:
            content = source_file.read()
        with open(destination_path, "w", encoding="utf-16") as dest_file:
            dest_file.write(content)

        # Use the copied file as the source for the return content
        read_path = destination_path
    else:
        read_path = file_path

    # Read the content
    with open(read_path, "r", encoding="utf-16") as file:
        content = file.read()
    
    filename = os.path.basename(read_path)
    return filename, content


def process_xml_file(file_path: str, copy_to: Optional[str] = None) -> ProcessedXMLFile:
    """
    Processes a single XML file: copies, reads, replaces event IDs, and extracts data.
    Args:
        file_path (str): Path to the XML file to process
        copy_to (Optional[str]): Directory to copy the file to
    Returns:
        ProcessedXMLFile: Processed file data
    """
    filename, original_content = copy_and_read_xml_file(file_path, copy_to)
    content_with_event_names, events_found = replace_event_ids_with_names(original_content)
    extracted_data = extract_data_about_report(content_with_event_names, events_found)
    
    return ProcessedXMLFile(
        filename=filename,
        original_content=original_content,
        content_with_event_names=content_with_event_names,
        events_found=events_found,
        extracted_data=extracted_data
    )


def read_xml_as_string(copy_to: Optional[str]) -> Tuple[str, str, str]:
    """
    Copies an XML file from a user-selected location and reads its content.
    Returns:
        Tuple[str, str, str]: (filename, content_with_event_names, extracted_data)
    """
    file_path = select_xml_file()
    
    if not file_path:
        raise FileNotFoundError("No file was selected.")

    processed_file = process_xml_file(file_path, copy_to)
    return processed_file.filename, processed_file.content_with_event_names, processed_file.extracted_data


def save_schema_as_json(report_to_save: dict, report_name: str, subdir_name: str, directory: str) -> None:
    """
    Saves the report schema as a JSON file.
    Args:
        report_to_save (dict): The report schema to save.
        report_name (str): The name of the report.
        directory (str): The directory to save the JSON file in.
    """
    directory = os.path.join(directory, subdir_name)
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Check if needs to add .json extension
    if not report_name.endswith(".json"):
        report_name += ".json"
    
    file_path = os.path.join(directory, report_name)
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(report_to_save, file, indent=2)
    print(f"Saved {report_name} to {directory}")

# fin.
