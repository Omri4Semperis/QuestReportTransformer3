from typing import Literal


class AmbiguousReportTypeError(Exception):
    """Custom exception for ambiguous report type inference."""

    def __init__(self, message: str):
        super().__init__(message)


def infer_db_report_type(
    DNS_filters: bool,
    DNS_displays: bool,
    NonDNS_filters: bool,
    NonDNS_displays: bool,
):
    something_about_dns = any([DNS_filters, DNS_displays])
    something_about_nondns = any([NonDNS_filters, NonDNS_displays])
    if something_about_dns and not something_about_nondns:
        return "DB_DNS"
    if something_about_nondns and not something_about_dns:
        return "DB_NonDNS"
    if something_about_dns and something_about_nondns:
        raise AmbiguousReportTypeError(
            "The user input contains both DNS and Non-DNS database-related queries, which is ambiguous. "
            "Please clarify whether the report should focus on DNS or Non-DNS details."
        )

    raise AmbiguousReportTypeError(
        "The user input does not provide enough information to determine the DB report type."
    )


def infer_report_type_from_user_input(
    current_status: bool,
    historical_changes: bool,
    DNS_filters: bool,
    DNS_displays: bool,
    NonDNS_filters: bool,
    NonDNS_displays: bool,
) -> Literal["LDAP", "DB_DNS", "DB_NonDNS"]:
    if current_status and not historical_changes:
        return "LDAP"

    if not current_status and historical_changes:
        return infer_db_report_type(
            DNS_filters=DNS_filters,
            DNS_displays=DNS_displays,
            NonDNS_filters=NonDNS_filters,
            NonDNS_displays=NonDNS_displays,
        )

    if current_status and historical_changes:
        raise AmbiguousReportTypeError(
            "The user input contains both current status and database-related queries, which is ambiguous. "
            "Please clarify whether the report should focus on LDAP or database details."
        )

    raise AmbiguousReportTypeError(
        "The user input does not provide enough information to determine the report type."
    )


def get_breakdown(query):
    from src.schemas.meta.report_type_hints import tools, ask_for_a_report

    response = ask_for_a_report(query, tools)

    pass
