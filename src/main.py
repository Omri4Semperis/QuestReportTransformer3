from typing import Dict, Literal

from files_management.files_handler import (
    get_artifacts_dir,
    read_xml_as_string,
    save_schema_as_jsons,
)
from utils.likely_report_types import get_likely_report_types


def main():
    artifacts_dir = get_artifacts_dir()
    quest_report_str = read_xml_as_string(copy_to=artifacts_dir)

    likely_report_types: Dict[
        Literal["LDAP", "DNS", "NonDNS"], Literal["yes", "no", "maybe"]
    ] = get_likely_report_types(quest_report_str)

    pass

    # generated_report = {
    #     "LDAP": [],
    #     "DNS": {1: {"this is": "schema a for dns"}, 2: {"this is": "schema b for dns"}},
    #     "NonDNS": {
    #         1: {"this is": "schema a for non-dns"},
    #         2: {"this is": "schema b for non-dns"},
    #         3: {"this is": "schema c for non-dns"},
    #     },
    # }

    generated_report = generate_reports_from_likely_report_types(
        likely_report_types=likely_report_types,
        quest_report_str=quest_report_str,
    )

    user_choice: Dict[str] = {
        "LDAP": [],
        "DNS": [2],
        "NonDNS": [1, 2, 3],
    }

    user_choice = ask_user_for_choices(generated_report=generated_report)

    save_schema_as_jsons(generated_report, user_choice)


if __name__ == "__main__":
    main()
