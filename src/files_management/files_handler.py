import datetime
from fileinput import filename
import os
import tkinter as tk
from tkinter import filedialog
from typing import Optional


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


def read_xml_as_string(copy_to: Optional[str]) -> str:
    """
    Copies an XML file from a user-selected location and reads its content.
    Returns:
        str: The content of the XML file as a string.
    """
    # Open a file dialog box to get the XML file path
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(
        title="Select an XML file",
        filetypes=[("XML files", "*.xml"), ("All files", "*.*")],
    )

    if not file_path:
        raise FileNotFoundError("No file was selected.")

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

    return content


def save_schema_as_jsons(generated_report: dict, user_choice: dict) -> None:
    pass
