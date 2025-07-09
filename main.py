from typing import Any, Dict, List, Literal
import json
from src.files_management.files_handler import (
    get_artifacts_dir,
    select_xml_file,
    process_xml_file,
    save_schema_as_json,
)
from src.utils.likely_report_types import get_likely_report_types
from src.utils.report_template_envocation import generate_reports_from_likely_report_types

# Constants
EXIT_COMMAND = 'exit'

def collect_xml_file_paths() -> List[str]:
    """
    Collects XML file paths from user selection.
    Returns:
        List[str]: List of selected file paths
    """
    file_paths = []
    print("Select XML files to process. Select files one by one, then cancel/close dialog when done.")
    
    while True:
        file_path = select_xml_file()
        if not file_path:
            # Empty path means user is done selecting
            break
        
        file_paths.append(file_path)
        print(f"Added: {file_path}")
    
    if not file_paths:
        print("No files selected.")
        return []
    
    # Present files and get user confirmation
    return confirm_file_selection(file_paths)


def confirm_file_selection(file_paths: List[str]) -> List[str]:
    """
    Presents selected files to user and allows modification.
    Returns:
        List[str]: Final list of file paths to process
    """
    while True:
        print(f"\n{len(file_paths)} files selected for processing:")
        for i, path in enumerate(file_paths, 1):
            print(f"  {i}. {path}")
        
        print("\nOptions:")
        print("  [r] followed by numbers - Remove files (e.g., 'r 1 3' removes files 1 and 3)")
        print("  [a] - Add more files")
        print("  [Enter] - Proceed with current selection")
        
        choice = input("Your choice: ").strip()
        
        if not choice:
            # Empty input means proceed
            break
        elif choice.lower().startswith('r'):
            file_paths = remove_files_by_numbers(file_paths, choice)
        elif choice.lower() == 'a':
            file_paths = add_more_files(file_paths)
        else:
            print("Invalid option. Please use 'r' followed by numbers, 'a', or press Enter.")
    
    return file_paths


def remove_files_by_numbers(file_paths: List[str], command: str) -> List[str]:
    """
    Removes files from the list based on user-specified numbers.
    Args:
        file_paths: Current list of file paths
        command: Command string like "r 1 3"
    Returns:
        List[str]: Updated list with specified files removed
    """
    try:
        # Extract numbers from command (skip the 'r' part)
        numbers_str = command[1:].strip()
        if not numbers_str:
            print("Please specify file numbers to remove (e.g., 'r 1 3')")
            return file_paths
        
        # Parse numbers
        numbers = [int(x.strip()) for x in numbers_str.split() if x.strip().isdigit()]
        if not numbers:
            print("Please specify valid file numbers to remove")
            return file_paths
        
        # Convert to 0-based indices and sort in reverse order
        indices_to_remove = sorted([n - 1 for n in numbers if 1 <= n <= len(file_paths)], reverse=True)
        
        if not indices_to_remove:
            print("No valid file numbers specified")
            return file_paths
        
        # Remove files
        for index in indices_to_remove:
            removed_file = file_paths.pop(index)
            print(f"Removed: {removed_file}")
        
        if not file_paths:
            print("All files removed. Please add some files.")
            return add_more_files([])
        
        return file_paths
    
    except ValueError:
        print("Invalid format. Use 'r' followed by numbers (e.g., 'r 1 3')")
        return file_paths


def add_more_files(current_files: List[str]) -> List[str]:
    """
    Allows user to add more files to the current selection.
    Args:
        current_files: Current list of file paths
    Returns:
        List[str]: Updated list with new files added
    """
    print("\nSelect additional files...")
    
    while True:
        file_path = select_xml_file()
        if not file_path:
            # Empty path means done adding
            break
        
        if file_path in current_files:
            print(f"File already selected: {file_path}")
            continue
        
        current_files.append(file_path)
        print(f"Added: {file_path}")
    
    return current_files


def calculate_min_unique_prefix_length(filenames: List[str]) -> int:
    """
    Find the minimum int n, such that taking the first n characters of each string in the list will produce a unique set of strings.
    """
    min_length = 5
    while True:
        seen = set()
        for s in filenames:
            if len(s) < min_length:
                return min_length
            prefix = s[:min_length]
            if prefix in seen:
                break
            seen.add(prefix)
        else:
            return min_length
        min_length += 1


def process_files_and_generate_reports(file_paths: List[str], artifacts_dir: str) -> None:
    """
    Processes all selected files and generates reports.
    Args:
        file_paths: List of file paths to process
        artifacts_dir: Directory to save artifacts
    """
    processed_files = {}
    
    # Process all files
    for file_path in file_paths:
        print(f"Pre-Processing: {file_path}")
        processed_file = process_xml_file(file_path, artifacts_dir)
        processed_files[processed_file.filename] = processed_file
    
    # Calculate subdirectory names
    filenames = list(processed_files.keys())
    min_prefix_length = calculate_min_unique_prefix_length(filenames)
    
    for filename in filenames:
        processed_files[filename].subdir_name = filename[:min(min_prefix_length, len(filename))]
    
    # Generate reports for all files
    for filename, processed_file in processed_files.items():
        print(f'\n{"#" * 50}')
        print(f"Generating reports for: {filename}")
        print(f'{"#" * 50}\n')
        
        likely_report_types: Dict[
            Literal["LDAP", "DNS", "NonDNS"], Literal["yes", "no", "maybe"]
        ] = get_likely_report_types(
            quest_report_str=processed_file.content_with_event_names, 
            extracted_data=processed_file.extracted_data
        )

        generated_reports: Dict[str, Dict[int, Any]] = generate_reports_from_likely_report_types(
            report_type_to_likelihood=likely_report_types,
            quest_report_str=processed_file.content_with_event_names,
            extracted_data=processed_file.extracted_data
        )
        
        for report_type, reports in generated_reports.items():
            print(f"{report_type}: {len(reports)} reports generated")
            for i, report_dict in enumerate(reports):
                report_name = f"{filename}_as_{report_type}_{i + 1}"
                save_schema_as_json(
                    report_to_save=report_dict,
                    report_name=report_name,
                    subdir_name=processed_file.subdir_name,
                    directory=artifacts_dir
                )


def main():
    """Main function to coordinate the file processing workflow."""
    artifacts_dir = get_artifacts_dir()
    
    # Collect all file paths first
    file_paths = collect_xml_file_paths()
    
    if not file_paths:
        print("No files selected. Exiting.")
        return
    
    print(f"\nProceeding with {len(file_paths)} files...")
    
    # Process all files and generate reports
    process_files_and_generate_reports(file_paths, artifacts_dir)

if __name__ == "__main__":
    main()

# fin.
