from typing import Any, Dict, Literal
import json
from src.files_management.files_handler import (
    get_artifacts_dir,
    read_xml_as_string,
    save_schema_as_json,
)
from src.utils.likely_report_types import get_likely_report_types
from src.utils.report_template_envocation import generate_reports_from_likely_report_types

def get_min_length_that_works(strings: list[str]) -> int:
    """
    Find the minimum int n, such that taking the first n characters of each string in the list will produce a unique set of strings.
    """
    min_length = 5
    while True:
        seen = set()
        for s in strings:
            if len(s) < min_length:
                return min_length
            prefix = s[:min_length]
            if prefix in seen:
                break
            seen.add(prefix)
        else:
            return min_length
        min_length += 1

def main():
    artifacts_dir = get_artifacts_dir()
    xmls = {}
    while True:
        file_name, quest_report_str, extracted_data = read_xml_as_string(copy_to=artifacts_dir)
        xmls[file_name] = {'quest_report_str': quest_report_str,
                           'extracted_data': extracted_data}
        if not file_name or input("Process another file or [e]xit? [e] for exit, else- process another:\n").strip().lower() == 'e':
            break           
    
    min_length_that_works = get_min_length_that_works(list(xmls.keys()))
    
    for file_name in xmls.keys():
        xmls[file_name]['subdir_name'] = file_name[:min(min_length_that_works, len(file_name))]
    
    for file_name, xml_data in xmls.items():
        quest_report_str = xml_data['quest_report_str']
        extracted_data = xml_data['extracted_data']
        process_title = f"Processing file: {file_name}"
        print('\n' + '#' * len(process_title) + '\n' + process_title + '\n')
        
        likely_report_types: Dict[
            Literal["LDAP", "DNS", "NonDNS"], Literal["yes", "no", "maybe"]
        ] = get_likely_report_types(xmls)

        generated_report: Dict[str, Dict[int, Any]] = generate_reports_from_likely_report_types(
            report_type_to_likelihood=likely_report_types,
            quest_report_str=quest_report_str,
            extracted_data=extracted_data
        )
        
        for report_type, reports in generated_report.items():
            print(f"{report_type}: {len(reports)} reports generated")
            for i, report_dict in enumerate(reports):
                name = f"{file_name}_as_{report_type}_{i + 1}"
                save_schema_as_json(report_to_save=report_dict,
                                    report_name=name,
                                    subdir_name=xml_data['subdir_name'],
                                    directory=artifacts_dir)
        
        # user_choice: Dict[str] = {
        #     "LDAP": [],
        #     "DNS": [2],
        #     "NonDNS": [1, 2, 3],
        # }

        # user_choice = ask_user_for_choices(generated_report=generated_report)

        # save_schema_as_jsons(generated_report, user_choice)


if __name__ == "__main__":
    main()
