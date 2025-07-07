from src.utils.azure_client_utils import ask_with_schema
from src.schemas.rat_report_schema.Content.LDAP_Content_schema import LDAPContentSchema
from src.schemas.rat_report_schema.MetaData.Meta_schema import MetaDataSchema

def get_ldap_content(
    quest_report_str:str, # This is the XML report string
    report_description,  # This is the free text extracted from the report
    ldap_query, # This is the LDAP query generated from the report
    desired_report_description, # This is a description of the desired report, including filters and display fields
    temperature: float, # Temperature for the model response
    ):

    prompt = f"""
    I want you to help me convert a report in one format, to another.
    
    Original report format:
    <original report format>{quest_report_str}</original report format>
    
    Report description:
    <report description>{report_description}</report description>
    
    LDAP query that is likely to be used in the report:
    <ldap query>{ldap_query}</ldap query>
    
    Here's some general information about the report I want to generate:
    {desired_report_description}
    """
    
    result = ask_with_schema(
        system_prompt="You are a helpful assistant, an expert of reports generation. Reply briefly according to the schema.",
        prompt=prompt,
        schema=LDAPContentSchema,
        temperature=temperature)
    
    return result

def get_ldap_meta(
    quest_report_str: str, # This is the XML report string
    report_description: str, # This is the free text extracted from the report
    ldap_query: str, # This is the LDAP query generated from the report
    desired_report_description: str, # This is a description of the desired report, including filters and display fields
    temperature: float, # Temperature for the model response
    report_content  # The content which was generated for this report
):
    return None