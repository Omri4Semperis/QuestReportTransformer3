from pydantic import BaseModel, Field

import pandas as pd
import os


class AmbiguousReportTypeError(Exception):
    """Custom exception for ambiguous report type inference."""

    def __init__(self, message: str):
        super().__init__(message)


# Read from knowledge directory at root
filters_df = pd.read_csv("knowledge/filters.csv")
displays_df = pd.read_csv("knowledge/display_fields.csv")


def summarize_filters(df: pd.DataFrame, DNS_or_NonDNS: str) -> str:
    # Check column exists
    if DNS_or_NonDNS not in df.columns:
        raise ValueError(f"Column '{DNS_or_NonDNS}' not found in DataFrame.")

    # Filter rows where DNS/NonDNS is True
    filtered_df = df[df[DNS_or_NonDNS] == True]

    # Build detailed summary
    lines = []
    for _, row in filtered_df.iterrows():
        # Compose description for this filter
        line = (
            f"- {row['filter']}: {row['description']}"
            f" Mandatory: {'Yes' if row['mandatory'] else 'No'}"
            f" Allowed States: {row['allowed_states']}"
            f" Input Modes: {row['input']}"
            f" Possible Values: {row['values']}"
        )
        lines.append(line)

    # Join all lines
    summary = "\n".join(lines)
    return summary


def summarize_displays(df: pd.DataFrame, DNS_or_NonDNS: str) -> str:
    # Check column exists
    if DNS_or_NonDNS not in df.columns:
        raise ValueError(f"Column '{DNS_or_NonDNS}' not found in DataFrame.")

    # Filter rows where DNS/NonDNS is True
    filtered_df = df[df[DNS_or_NonDNS] == True]

    # Group by category_name
    grouped = filtered_df.groupby("category_name")

    # Build summary lines
    lines = []
    count = 1
    for idx, (category, group_df) in enumerate(grouped, start=1):
        lines.append(f"Category #{idx}: {category}")
        for _, row in group_df.iterrows():
            lines.append(f"  {count}. {row['field']}: {row['description']}")
            count += 1

    # Join all lines into one string
    summary = "\n".join(lines).strip()
    return summary


dns_filters_summary: str = summarize_filters(filters_df, "DNS")
dns_displays_summary: str = summarize_displays(displays_df, "DNS")
non_dns_filters_summary: str = summarize_filters(filters_df, "NonDNS")
non_dns_displays_summary: str = summarize_displays(displays_df, "NonDNS")

current_status_description: str = (
    "Is the request asking for the current status of Active Directory? Has the user indicated that they're interested in something that's currently happening? Current status requests are anything that can be querried using LDAP."
)
historical_changes_description: str = (
    "Is the request asking for historical Active Directory changes? Things that cannot be revealed having only current access to Active Directory using LDAP, but require historical data to answer. e.g. Asking for changes in the last 30 days, or changes made by a specific user in the last year, etc."
)
DNS_filters_description: str = (
    f"Is the request asking for DNS filters? DNS filters are:\n{dns_filters_summary}"
)
DNS_displays_description: str = (
    f"Is the request asking for DNS displays? DNS displays are:\n{dns_displays_summary}"
)
NonDNS_filters_description: str = (
    f"Is the request asking for Non-DNS filters? Non-DNS filters are:\n{non_dns_filters_summary}"
)
NonDNS_displays_description: str = (
    f"Is the request asking for Non-DNS displays? Non-DNS displays are:\n{non_dns_displays_summary}"
)


class ReportTypeHints(BaseModel):
    """Schema for RAT reports."""

    asked_for_current_status: bool = Field(description=current_status_description)
    asked_for_historical_changes: bool = Field(
        description=historical_changes_description
    )
    asked_for_DNS_filters: bool = Field(description=DNS_filters_description)
    asked_for_DNS_displays: bool = Field(description=DNS_displays_description)
    asked_for_NonDNS_filters: bool = Field(description=NonDNS_filters_description)
    asked_for_NonDNS_displays: bool = Field(description=NonDNS_displays_description)

    comment: str = Field(description="Explain your reasoning for the above choices.")
    feedback: str = Field(
        description="Any feedback you like, but be concise. This is not mandatory."
    )
