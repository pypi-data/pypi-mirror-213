from ms_salesforce_api.salesforce.project.dto.ProjectLineItemDTO import (  # noqa: E501
    ProjectLineItemDTO,
)


class OpportunityDTO(object):
    def __init__(
        self,
        client_fiscal_name,
        client_account_name,
        currency,
        amount,
        invoicing_country_code,
        operation_coordinator_email,
        operation_coordinator_sub_email,
        created_at,
        last_updated_at,
        opportunity_name,
        stage,
        account_billing_country,
        lead_source,
        project_code,
        project_id,
        project_name,
        project_start_date,
        controller_email,
        controller_sub_email,
        profit_center,
        cost_center,
        project_tier,
        jira_task_url,
        opportunity_percentage,
        account_assigment_group,
        account_tax_category,
        account_tax_classification,
        account_txt_sapid,
        account_business_function,
        account_tax_id_type,
        account_currency_code,
        account_created_date,
        account_tier,
        account_pec_email,
        account_phone,
        account_fax,
        account_website,
        account_cif,
        account_billing_address,
        account_billing_city,
        account_billing_postal_code,
        account_billing_street,
        account_company_invoicing,
        account_office,
        account_payment_terms,
        account_billing_state_code,
        account_mail_invoicing,
        account_invoicing_email,
        billing_lines=[],
        project_line_items=[],
    ):
        self.client_fiscal_name = client_fiscal_name
        self.client_account_name = client_account_name
        self.currency = currency
        self.amount = amount
        self.invoicing_country_code = invoicing_country_code
        self.operation_coordinator_email = operation_coordinator_email
        self.operation_coordinator_sub_email = operation_coordinator_sub_email
        self.created_at = created_at
        self.last_updated_at = last_updated_at
        self.opportunity_name = opportunity_name
        self.stage = stage
        self.account_billing_country = account_billing_country
        self.lead_source = lead_source
        self.project_code = project_code
        self.project_id = project_id
        self.project_name = project_name
        self.project_start_date = project_start_date
        self.controller_email = controller_email
        self.controller_sub_email = controller_sub_email
        self.profit_center = profit_center
        self.cost_center = cost_center
        self.project_tier = project_tier
        self.jira_task_url = jira_task_url
        self.opportunity_percentage = opportunity_percentage
        self.billing_lines = billing_lines
        self.project_line_items = project_line_items
        self.account_assigment_group = account_assigment_group
        self.account_tax_category = account_tax_category
        self.account_tax_classification = account_tax_classification
        self.account_txt_sapid = account_txt_sapid
        self.account_business_function = account_business_function
        self.account_tax_id_type = account_tax_id_type
        self.account_currency_code = account_currency_code
        self.account_created_date = account_created_date
        self.account_tier = account_tier
        self.account_pec_email = account_pec_email
        self.account_phone = account_phone
        self.account_fax = account_fax
        self.account_website = account_website
        self.account_cif = account_cif
        self.account_billing_address = account_billing_address
        self.account_billing_city = account_billing_city
        self.account_billing_postal_code = account_billing_postal_code
        self.account_billing_street = account_billing_street
        self.account_company_invoicing = account_company_invoicing
        self.account_office = account_office
        self.account_payment_terms = account_payment_terms
        self.account_billing_state_code = account_billing_state_code
        self.account_mail_invoicing = account_mail_invoicing
        self.account_invoicing_email = account_invoicing_email

    @staticmethod
    def from_salesforce_record(record):
        def _normalize_str(text):
            try:
                return (
                    text.replace("\n", "").replace("\r", "").replace("'", "")
                )
            except AttributeError:
                return text

        def _get_client_fiscal_name():
            try:
                return record["Project_Account__r"]["Business_Name__c"]
            except (TypeError, KeyError):
                return ""

        def _get_client_account_name():
            try:
                return record["Project_Account__r"]["Name"]
            except (TypeError, KeyError):
                return ""

        def _get_account_billing_country():
            try:
                return record["Project_Account__r"]["BillingCountryCode"]
            except (TypeError, KeyError):
                return ""

        def _get_account_assigment_group():
            try:
                return record["Project_Account__r"][
                    "MS_Customer_Account_Assigment_Group__c"
                ]
            except (TypeError, KeyError):
                return ""

        def _get_account_tax_category():
            try:
                return record["Project_Account__r"][
                    "MS_Customer_Tax_Category__c"
                ]
            except (TypeError, KeyError):
                return ""

        def _get_account_tax_classification():
            try:
                return record["Project_Account__r"][
                    "MS_Customer_Tax_Classification__c"
                ]
            except (TypeError, KeyError):
                return ""

        def _get_account_txt_sapid():
            try:
                return record["Project_Account__r"]["TXT_SAPId__c"]
            except (TypeError, KeyError):
                return ""

        def _get_account_business_function():
            try:
                return record["Project_Account__r"]["ms_Business_Function__c"]
            except (TypeError, KeyError):
                return ""

        def _get_account_tax_id_type():
            try:
                return record["Project_Account__r"]["ms_TAX_id_Type__c"]
            except (TypeError, KeyError):
                return ""

        def _get_account_currency_code():
            try:
                return record["Project_Account__r"]["CurrencyISOCode"]
            except (TypeError, KeyError):
                return ""

        def _get_account_created_date():
            try:
                return record["Project_Account__r"]["CreatedDate"]
            except (TypeError, KeyError):
                return ""

        def _get_account_tier():
            try:
                return record["Project_Account__r"]["Tier__c"]
            except (TypeError, KeyError):
                return ""

        def _get_account_pec_email():
            try:
                return record["Project_Account__r"]["PEC_Email__c"]
            except (TypeError, KeyError):
                return ""

        def _get_account_phone():
            try:
                return record["Project_Account__r"]["Phone"]
            except (TypeError, KeyError):
                return ""

        def _get_account_fax():
            try:
                return record["Project_Account__r"]["Fax"]
            except (TypeError, KeyError):
                return ""

        def _get_account_website():
            try:
                return record["Project_Account__r"]["Website"]
            except (TypeError, KeyError):
                return ""

        def _get_account_cif():
            try:
                return record["Project_Account__r"]["CIF__c"]
            except (TypeError, KeyError):
                return ""

        def _get_account_billing_address():
            def build_address(location_dict):
                """
                Construct a string representation of an address from a
                dictionary.

                :param location_dict: a dictionary containing location
                information.
                :return: a string representing the address.
                """
                address_components = []

                for field in [
                    "street",
                    "city",
                    "state",
                    "postalCode",
                    "country",
                ]:
                    if field in location_dict and location_dict.get(field, ""):
                        address_components.append(location_dict[field])

                address = ", ".join(address_components)

                return _normalize_str(address)

            try:
                return build_address(
                    record["Project_Account__r"]["BillingAddress"]
                )
            except (TypeError, KeyError):
                return ""

        def _get_account_billing_city():
            try:
                return record["Project_Account__r"]["BillingCity"]
            except (TypeError, KeyError):
                return ""

        def _get_account_billing_postal_code():
            try:
                return record["Project_Account__r"]["BillingPostalCode"]
            except (TypeError, KeyError):
                return ""

        def _get_account_billing_street():
            try:
                return _normalize_str(
                    record["Project_Account__r"]["BillingStreet"]
                )
            except (TypeError, KeyError):
                return ""

        def _get_account_company_invoicing():
            try:
                return record["Project_Account__r"]["MS_Company_Invoicing__c"]
            except (TypeError, KeyError):
                return ""

        def _get_account_office():
            try:
                return record["Project_Account__r"]["MS_Office__c"]
            except (TypeError, KeyError):
                return ""

        def _get_account_payment_terms():
            try:
                return record["Project_Account__r"]["Payment_Terms__c"]
            except (TypeError, KeyError):
                return ""

        def _get_account_billing_state_code():
            try:
                return record["Project_Account__r"]["BillingStateCode"]
            except (TypeError, KeyError):
                return ""

        def _get_account_mail_invoicing():
            try:
                return record["Project_Account__r"]["MAIL_Invoicing__c"]
            except (TypeError, KeyError):
                return ""

        def _get_account_invoicing_email():
            try:
                email = record["Project_Account__r"]["Invoicing_Email__c"]
                if email:
                    return email.replace("\n", ",").replace("\r", "")
            except (TypeError, KeyError):
                return ""

        def _get_operation_coordinator_email():
            try:
                return record["Operation_Coordinator__r"]["Name"]
            except (TypeError, KeyError):
                return ""

        def _get_operation_coordinator_sub_email():
            try:
                return record["Operation_Coordinator_Sub__r"]["Name"]
            except (TypeError, KeyError):
                return ""

        def _get_opportunity_name():
            try:
                return record["Opportunity__r"]["Opportunity_Name_Short__c"]
            except (TypeError, KeyError):
                return ""

        def _get_stage():
            try:
                return record["Opportunity__r"]["StageName"]
            except (TypeError, KeyError):
                return ""

        def _get_lead_source():
            try:
                return record["Opportunity__r"]["LeadSource"]
            except (TypeError, KeyError):
                return ""

        def _get_controller_email():
            try:
                return record["Operation_Coordinator__r"]["Controller__c"]
            except (TypeError, KeyError):
                return ""

        def _get_controller_sub_email():
            try:
                return record["Operation_Coordinator_Sub__r"][
                    "Controller_SUB__c"
                ]
            except (TypeError, KeyError):
                return ""

        def _get_project_tier():
            try:
                return record["Opportunity__r"]["Tier_Short__c"]
            except (TypeError, KeyError):
                return ""

        def _get_jira_task_url():
            try:
                return record["Opportunity__r"]["JiraComponentURL__c"]
            except (TypeError, KeyError):
                return ""

        def _get_opportunity_percentage():
            try:
                return record["Opportunity__r"]["Probability"]
            except (TypeError, KeyError):
                return ""

        project_line_items = (
            [
                ProjectLineItemDTO.from_salesforce_record(item)
                for item in record.get("Project_Line_Items__r", {}).get(
                    "records", []
                )
            ]
            if record.get("Project_Line_Items__r")
            else []
        )

        return OpportunityDTO(
            client_fiscal_name=_get_client_fiscal_name(),
            client_account_name=_get_client_account_name(),
            currency=record["CurrencyIsoCode"],
            amount=record.get("Total_Project_Amount__c", 0),
            invoicing_country_code=record["Invoicing_Country_Code__c"],
            operation_coordinator_email=_get_operation_coordinator_email(),
            operation_coordinator_sub_email=_get_operation_coordinator_sub_email(),  # noqa: E501
            created_at=record["CreatedDate"],
            last_updated_at=record["LastModifiedDate"],
            opportunity_name=_get_opportunity_name(),
            stage=_get_stage(),
            account_billing_country=_get_account_billing_country(),
            lead_source=_get_lead_source(),
            project_code=record["FRM_MSProjectCode__c"],
            project_id=record["Id"],
            project_name=record["Name"],
            project_start_date=record["Start_Date__c"],
            controller_email=_get_controller_email(),
            controller_sub_email=_get_controller_sub_email(),
            profit_center=record["Profit_Center__c"],
            cost_center=record["Cost_Center__c"],
            project_tier=_get_project_tier(),
            jira_task_url=_get_jira_task_url(),
            opportunity_percentage=_get_opportunity_percentage(),
            project_line_items=project_line_items,
            account_assigment_group=_get_account_assigment_group(),
            account_tax_category=_get_account_tax_category(),
            account_tax_classification=_get_account_tax_classification(),
            account_txt_sapid=_get_account_txt_sapid(),
            account_business_function=_get_account_business_function(),
            account_tax_id_type=_get_account_tax_id_type(),
            account_currency_code=_get_account_currency_code(),
            account_created_date=_get_account_created_date(),
            account_tier=_get_account_tier(),
            account_pec_email=_get_account_pec_email(),
            account_phone=_get_account_phone(),
            account_fax=_get_account_fax(),
            account_website=_get_account_website(),
            account_cif=_get_account_cif(),
            account_billing_address=_get_account_billing_address(),
            account_billing_city=_get_account_billing_city(),
            account_billing_postal_code=_get_account_billing_postal_code(),
            account_billing_street=_get_account_billing_street(),
            account_company_invoicing=_get_account_company_invoicing(),
            account_office=_get_account_office(),
            account_payment_terms=_get_account_payment_terms(),
            account_billing_state_code=_get_account_billing_state_code(),
            account_mail_invoicing=_get_account_mail_invoicing(),
            account_invoicing_email=_get_account_invoicing_email(),
        )

    def add_billing_lines(self, billing_lines):
        self.billing_lines.extend(billing_lines)

    def to_dict(self):
        return {
            "client_fiscal_name": self.client_fiscal_name,
            "client_account_name": self.client_account_name,
            "currency": self.currency,
            "amount": self.amount,
            "invoicing_country_code": self.invoicing_country_code,
            "operation_coordinator_email": self.operation_coordinator_email,
            "operation_coordinator_sub_email": self.operation_coordinator_sub_email,  # noqa: E501
            "created_at": self.created_at,
            "last_updated_at": self.last_updated_at,
            "opportunity_name": self.opportunity_name,
            "stage": self.stage,
            "account_billing_country": self.account_billing_country,
            "lead_source": self.lead_source,
            "project_code": self.project_code,
            "project_id": self.project_id,
            "project_name": self.project_name,
            "project_start_date": self.project_start_date,
            "controller_email": self.controller_email,
            "controller_sub_email": self.controller_sub_email,
            "profit_center": self.profit_center,
            "cost_center": self.cost_center,
            "project_tier": self.project_tier,
            "jira_task_url": self.jira_task_url,
            "opportunity_percentage": self.opportunity_percentage,
            "billing_lines": [bl.to_dict() for bl in self.billing_lines],
            "project_line_items": [
                pli.to_dict() for pli in self.project_line_items
            ],
            "account_assigment_group": self.account_assigment_group,
            "account_tax_category": self.account_tax_category,
            "account_tax_classification": self.account_tax_classification,
            "account_txt_sapid": self.account_txt_sapid,
            "account_business_function": self.account_business_function,
            "account_tax_id_type": self.account_tax_id_type,
            "account_currency_code": self.account_currency_code,
            "account_created_date": self.account_created_date,
            "account_tier": self.account_tier,
            "account_pec_email": self.account_pec_email,
            "account_phone": self.account_phone,
            "account_fax": self.account_fax,
            "account_website": self.account_website,
            "account_cif": self.account_cif,
            "account_billing_address": self.account_billing_address,
            "account_billing_city": self.account_billing_city,
            "account_billing_postal_code": self.account_billing_postal_code,
            "account_billing_street": self.account_billing_street,
            "account_company_invoicing": self.account_company_invoicing,
            "account_office": self.account_office,
            "account_payment_terms": self.account_payment_terms,
            "account_billing_state_code": self.account_billing_state_code,
            "account_mail_invoicing": self.account_mail_invoicing,
            "account_invoicing_email": self.account_invoicing_email,
        }
