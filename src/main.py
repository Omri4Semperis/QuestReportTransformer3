from typing import Any, Dict, Literal

from files_management.files_handler import (
    get_artifacts_dir,
    read_xml_as_string,
    save_schema_as_jsons,
)
from utils.likely_report_types import get_likely_report_types
from utils.report_template_envocation import generate_reports_from_likely_report_types

def main():
    artifacts_dir = get_artifacts_dir()
    quest_report_str, extracted_data = read_xml_as_string(copy_to=artifacts_dir)

    likely_report_types: Dict[
        Literal["LDAP", "DNS", "NonDNS"], Literal["yes", "no", "maybe"]
    ] = get_likely_report_types(quest_report_str, extracted_data)

    pass

    # generated_report = {
    #     "LDAP": {},
    #     "DNS": {1: SCHEMA_!, 2: SCHEMA_2},
    #     "NonDNS": {
    #         1: this_is_SCHEMA_#1_for_non_dns_reports,
    #         2: this_is_SCHEMA_#2_for_non_dns_reports,
    #         3: this_is_SCHEMA_#3_for_non_dns_reports,
    #     },
    # }

    generated_report: Dict[str, Dict[int, Any]] = generate_reports_from_likely_report_types(
        report_type_to_likelihood=likely_report_types,
        quest_report_str=quest_report_str,
        extracted_data=extracted_data
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
