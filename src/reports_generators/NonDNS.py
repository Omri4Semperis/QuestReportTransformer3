from post_processing.metadata import post_process_metadata
from src.utils.azure_client_utils import ask_with_schema
from src.schemas.rat_report_schema.Content.NonDNS_Content_schema import NonDNSContentSchema
from src.schemas.rat_report_schema.MetaData.Meta_schema import MetaDataSchema

def get_nondns_content(
    quest_report_str:str, # This is the XML report string
    report_description,  # This is the free text extracted from the report
    description_of_an_nondns_report, # This is a description of the desired report, including filters and display fields
    temperature: float, # Temperature for the model response
    ):

    prompt = f"""
    I want you to help me convert a report in one format, to another.
    
    Original report format:
    <original report format>{quest_report_str}</original report format>
    
    Report description:
    <report description>{report_description}</report description>
    
    Here's some general information about the report I want to generate:
    {description_of_an_nondns_report}
    """
    
    result = ask_with_schema(
        system_prompt="You are a helpful assistant, an expert of reports generation. Reply briefly according to the schema.",
        prompt=prompt,
        schema=NonDNSContentSchema,
        temperature=temperature)
    
    return result

def get_nondns_meta(
    quest_report_str: str, # This is the XML report string
    report_description: str, # This is the free text extracted from the report
    temperature: float, # Temperature for the model response
    the_content_field_of_the_nondns_report  # The content which was generated for this report
):
    prompt = f"""
    I took an original xml report and turned it into my own json format. You will help me generate the metadata for this report.
    
    Original report format:
    <original report format>{quest_report_str}</original report format>
    
    Original report description:
    <report description>{report_description}</report description>
        
    Here is the content of the report I generated:
    <report content>{the_content_field_of_the_nondns_report}</report content>
    
    Follow the schema and generate the metadata for the report.
    """
    meta = ask_with_schema(
        system_prompt="You are a helpful assistant, an expert of reports generation. Reply briefly according to the schema.",
        prompt=prompt,
        schema=MetaDataSchema,
        temperature=temperature)

    return meta

def nondns_post_process(report):
    # TODO Implement any post-processing steps for the NonDNS report here
    report["MetaData"] = post_process_metadata(report["MetaData"])
    return report