from typing import List, Tuple
import tkinter as tk
from tkinter import filedialog
import os
from inference_utils import get_breakdown, infer_report_type_from_user_input
from schemas.meta.quest_report_analysis_schema import ReportTypeHints


def load_quest_report_as_str() -> str:
    """Opens a file dialog box, allowing the user to select a Quest report file (.xml format) and returns its content as a string."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    file_path = filedialog.askopenfilename(
        title="Select Quest Report File",
        filetypes=[("XML files", "*.xml")],
    )

    if not file_path:
        raise FileNotFoundError("No file selected.")

    with open(file_path, "r", encoding="latin-1") as file:
        quest_report_str = file.read()

    return quest_report_str


def ask_about_quest_report_format(
    client,
    model_name,
    breakdown_tools,
    quest_report_str: str,
    clarifications: List[str] = None,
) -> Tuple[bool, str]:
    prompt = "Help me understand this report format?\n<xml file starts here>\n{quest_report_str}\n<xml file ends here>"
    if clarifications:
        prompt += "\n\nClarifications:\n" + "\n".join(clarifications)
    breakdown = get_breakdown(
        client,
        model_name,
        prompt,
        tools=breakdown_tools,
    )

    infered_successfully, inference_result = infer_report_type_from_user_input(
        current_status=breakdown.get("asked_for_current_status", False),
        historical_changes=breakdown.get("asked_for_historical_changes", False),
        DNS_filters=breakdown.get("asked_for_DNS_filters", False),
        DNS_displays=breakdown.get("asked_for_DNS_displays", False),
        NonDNS_filters=breakdown.get("asked_for_NonDNS_filters", False),
        NonDNS_displays=breakdown.get("asked_for_NonDNS_displays", False),
    )

    pass


def process_report(quest_report_str: str, assumed_report_type: str):
    pass
    return None


def client_setup():
    from dotenv import load_dotenv
    from openai import AzureOpenAI

    load_dotenv()

    api_key = os.getenv("AZURE_API_KEY")
    api_version = os.getenv("AZURE_API_VERSION")
    azure_endpoint = os.getenv("AZURE_API_BASE")
    deployment_name = "gpt-4o"  # As specified in the original script

    # Initialize the Azure OpenAI client
    client = AzureOpenAI(
        api_key=api_key.strip(),
        api_version=api_version.strip(),
        azure_endpoint=azure_endpoint.strip(),
        timeout=30.0,
    )

    return client, deployment_name


def main():
    client, deployment_name = client_setup()

    quest_report_str = load_quest_report_as_str()

    breakdown_tools = [
        {
            "type": "function",
            "function": {
                "name": "get_breakdown_schema",
                "description": "Get the Report Breakdown schema based on user input.",
                "parameters": ReportTypeHints.model_json_schema(),
            },
        }
    ]

    infered_successfully = False
    clarifications: List[str] = []

    for attempt in range(3):
        infered_successfully, inference_feedback = ask_about_quest_report_format(
            client,
            deployment_name,
            breakdown_tools,
            quest_report_str,
            clarifications=clarifications,
        )
        if infered_successfully:
            break

        print("Inference failed:", inference_feedback)
        print(
            "Please clarify your request to help overcome the ambiguity, which will be added to the original input:"
        )
        user_input = input("Clarification: ")
        clarifications.append(user_input)

    if not infered_successfully:
        raise RuntimeError(
            "User input does not provide enough information to determine the report type. Terminating."
        )

    process_outcome: dict = process_report(
        client, quest_report_str, assumed_report_type=inference_feedback
    )

    return process_outcome


if __name__ == "__main__":
    outcome = main()
    print(outcome)
