import deepdiff
import tkinter as tk
import json

def compare_dicts(dict1, dict2):
    """
    Compare two dictionaries and return the differences.
    
    Args:
        dict1 (dict): The first dictionary to compare.
        dict2 (dict): The second dictionary to compare.
    
    Returns:
        dict: A dictionary containing the differences.
    """
    diff = deepdiff.DeepDiff(dict1, dict2, ignore_order=True)
    return diff

if __name__ == "__main__":
    # Ask for first path using a dialog box
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    path1 = tk.filedialog.askopenfilename(title="Select first JSON file")
    if not path1:
        print("No file selected for the first path.")
        exit(1)
    path2 = tk.filedialog.askopenfilename(title="Select second JSON file")
    if not path2:
        print("No file selected for the second path.")
        exit(1)
    # Load the JSON files
    with open(path1, 'r') as file1:
        dict1 = json.load(file1)
    with open(path2, 'r') as file2:
        dict2 = json.load(file2)
    # Compare the dictionaries
    differences = compare_dicts(dict1, dict2)
    # Print the differences
    if differences:
        print("Differences found:")
        print(json.dumps(differences, indent=2))