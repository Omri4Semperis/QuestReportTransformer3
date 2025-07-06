import re


def generate_ldap_report(quest_report_str: str, temperature: float) -> str:
    


def get_reports(
    report_type: str, likely_report_types: dict, quest_report_str: str
) -> list:
    temperatures = {
        "yes": [0, 0.2],
        "maybe": [0.0],
        "no": [],
    }.likely_report_types["LDAP"]

    func = {
        "LDAP": generate_ldap_report,
        "DNS": generate_dns_report,
        "NonDNS": generate_nondns_report,
    }.get(report_type, None)

    results = []

    for temperature in temperatures:
        report = func(quest_report_str, temperature)
        results.append(report)

    return results


def generate_reports_from_likely_report_types(
    report_type_to_likelihood: dict,
    quest_report_str: str,
):
    generated_report = {}
    for report_type in report_type_to_likelihood:
        generated_report[report_type] = get_reports(
            report_type, report_type_to_likelihood[report_type], quest_report_str
        )
    return generated_report
