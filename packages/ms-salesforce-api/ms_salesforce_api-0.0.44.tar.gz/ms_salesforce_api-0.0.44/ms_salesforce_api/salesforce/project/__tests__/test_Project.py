# flake8: noqa: E501
import unittest
from unittest.mock import patch

from ms_salesforce_api.salesforce.project import OpportunityDTO, Project

EXAMPLE_RESPONSE = [
    {
        "attributes": {
            "type": "Project__c",
            "url": "/services/data/v57.0/sobjects/Project__c/a003X000015kaPxQAI",
        },
        "Project_Account__r": {
            "attributes": {
                "type": "Account",
                "url": "/services/data/v57.0/sobjects/Account/001Aa000007ZP7bIAG",
            },
            "Business_Name__c": "ESMProjectAcc",
            "Name": "ESMProjectAccount",
            "BillingCountryCode": "ES",
        },
        "CurrencyIsoCode": "EUR",
        "Invoicing_Country_Code__c": "ES",
        "Operation_Coordinator__r": {
            "attributes": {
                "type": "Operation_Coordinator__c",
                "url": "/services/data/v57.0/sobjects/Operation_Coordinator__c/a0uAa000000CmAXIA0",
            },
            "Name": "jhon.doe@ext.makingscience.com",
            "Controller__c": "jhon.doe@ext.makingscience.com",
        },
        "Operation_Coordinator_Sub__r": {
            "attributes": {
                "type": "Operation_Coordinator__c",
                "url": "/services/data/v57.0/sobjects/Operation_Coordinator__c/a0uAa000000CmAXIA0",
            },
            "Name": "jhon.doe@ext.makingscience.com",
            "Controller_SUB__c": "jhon.doe@ext.makingscience.com",
        },
        "CreatedDate": "2020-07-14T12:55:56.000+0000",
        "LastModifiedDate": "2023-05-16T13:18:04.000+0000",
        "Opportunity__r": {
            "attributes": {
                "type": "Opportunity",
                "url": "/services/data/v57.0/sobjects/Opportunity/006Aa000004n3YjIAI",
            },
            "Opportunity_Name_Short__c": "ESMOPP",
            "StageName": "Qualification",
            "LeadSource": "Other",
            "Probability": 10.0,
            "Tier_Short__c": "Unkown",
            "JiraComponentURL__c": '<a href="https://makingscience.atlassian.net/browse/ESMSBD0001-11848" target="_blank">View Jira Task</a>',
        },
        "FRM_MSProjectCode__c": "ESMSEX00430",
        "Name": "ESMProject",
        "Id": "a003X000015kaPxQAI",
        "Start_Date__c": "2023-05-13",
        "Profit_Center__c": None,
        "Cost_Center__c": None,
        "Project_Line_Items__r": {
            "totalSize": 1,
            "done": True,
            "records": [
                {
                    "attributes": {
                        "type": "ProjectLineItem__c",
                        "url": "/services/data/v57.0/sobjects/ProjectLineItem__c/a0VAa000000fWbdMAE",
                    },
                    "Id": "a0VAa000000fWbdMAE",
                    "CreatedDate": "2023-05-13T09:03:14.000+0000",
                    "LastModifiedDate": "2023-05-16T13:18:01.000+0000",
                    "Duration_months__c": None,
                    "ProductNew__r": {
                        "attributes": {
                            "type": "Product2",
                            "url": "/services/data/v57.0/sobjects/Product2/01tAa0000010VZVIA2",
                        },
                        "Name": "ESM PRODUCT",
                    },
                    "Starting_Date__c": "2023-05-13",
                    "Cost_Center__c": None,
                    "Profit_Center__c": None,
                    "Business_Unit__c": None,
                    "Quantity__c": 12.0,
                    "UnitPrice__c": 90.0,
                    "Total_Price__c": 1080.0,
                    "Ending_Date__c": "2023-05-27",
                    "Department__c": None,
                    "Sales_Order_Item__c": 10.0,
                    "End_Date__c": "2023-05-27",
                    "Revenue_Type__c": "PS06",
                    "Effort__c": "12",
                    "Total_Billing_Amount_Billing_Lines__c": 90.0,
                    "MS_PLI_Name__c": "_MSEX00430",
                    "SapNetAmount__c": None,
                    "Country__c": "Spain",
                }
            ],
        },
    }
]
EXAMPLE_BILLING_LINES = [
    {
        "attributes": {
            "type": "Billing_Line__c",
            "url": "/services/data/v57.0/sobjects/Billing_Line__c/a0sAa0000004Lx7IAE",
        },
        "Id": "a0sAa0000004Lx7IAE",
        "Name": "BL-000320965",
        "Project_Line_Item__r": {
            "attributes": {
                "type": "ProjectLineItem__c",
                "url": "/services/data/v57.0/sobjects/ProjectLineItem__c/a0VAa000000fWbdMAE",
            },
            "Project__c": "a003X000015kaPxQAI",
        },
        "CurrencyIsoCode": "EUR",
        "CreatedDate": "2023-05-13T09:04:20.000+0000",
        "LastModifiedDate": "2023-05-13T09:04:20.000+0000",
        "Biling_Ammount__c": 90.0,
        "Billing_Date__c": "2023-05-13",
        "Billing_Period_Ending_Date__c": "2023-05-27",
        "Billing_Period_Starting_Date__c": "2023-05-13",
        "Hourly_Price__c": None,
        "Revenue_Dedication__c": None,
        "BillingPlanAmount__c": "90",
        "BillingPlanBillingDate__c": "2023-05-13",
        "BillingPlanItem__c": "12345",
        "BillingPlanServiceEndDate__c": "2023-05-27",
        "BillingPlanServiceStartDate__c": "2023-05-13",
    }
]


def mock_fetch_data(query):
    if "Project_Line_Items__r" in query:
        return EXAMPLE_RESPONSE
    elif "Project_Line_Item__r.Project__c" in query:
        return EXAMPLE_BILLING_LINES
    else:
        return None


class TestProject(unittest.TestCase):
    @patch(
        "ms_salesforce_api.salesforce.project.SalesforceQueryExecutor.authenticate"  # noqa: E501
    )
    @patch.object(Project, "fetch_data", side_effect=mock_fetch_data)
    def test_get_opportunities(self, mock_make_request, mock_authenticate):
        mock_authenticate.return_value = "access_token"

        client_id = "client_id"
        username = "username"
        domain = "https://auth.example.com"
        private_key = "private_key"

        project = Project(
            client_id,
            username,
            domain,
            private_key,
            audience="https://login.salesforce.com",
        )
        opportunities = project.get_opportunities(format="dto")
        self.assertEqual(len(opportunities), 1)

        opportunity = opportunities[0]
        self.assertIsInstance(opportunity, OpportunityDTO)
        self.assertEqual(
            opportunity.client_fiscal_name,
            "ESMProjectAcc",
        )
        self.assertEqual(opportunity.client_account_name, "ESMProjectAccount")
        self.assertEqual(opportunity.currency, "EUR")
        self.assertEqual(opportunity.amount, 0)
        self.assertEqual(opportunity.invoicing_country_code, "ES")
        self.assertEqual(
            opportunity.operation_coordinator_email,
            "jhon.doe@ext.makingscience.com",
        )
        self.assertEqual(
            opportunity.operation_coordinator_sub_email,
            "jhon.doe@ext.makingscience.com",
        )
        self.assertEqual(
            opportunity.created_at, "2020-07-14T12:55:56.000+0000"
        )
        self.assertEqual(
            opportunity.last_updated_at, "2023-05-16T13:18:04.000+0000"
        )
        self.assertEqual(opportunity.opportunity_name, "ESMOPP")
        self.assertEqual(opportunity.stage, "Qualification")
        self.assertEqual(opportunity.billing_country, "ES")
        self.assertEqual(opportunity.lead_source, "Other")
        self.assertEqual(opportunity.project_code, "ESMSEX00430")
        self.assertEqual(opportunity.project_id, "a003X000015kaPxQAI")
        self.assertEqual(opportunity.project_name, "ESMProject")
        self.assertEqual(opportunity.project_start_date, "2023-05-13")
        self.assertEqual(
            opportunity.controller_email, "jhon.doe@ext.makingscience.com"
        )
        self.assertEqual(
            opportunity.controller_sub_email, "jhon.doe@ext.makingscience.com"
        )
        self.assertIsNone(opportunity.profit_center)
        self.assertIsNone(opportunity.cost_center)
        self.assertEqual(opportunity.project_tier, "Unkown")
        self.assertEqual(
            opportunity.jira_task_url,
            '<a href="https://makingscience.atlassian.net/browse/ESMSBD0001-11848" target="_blank">View Jira Task</a>',  # noqa: E501
        )
        self.assertEqual(opportunity.opportunity_percentage, 10.0)
        self.assertEqual(len(opportunity.billing_lines), 1)
        billing_line = opportunity.billing_lines[0]

        self.assertEqual(billing_line.id, "a0sAa0000004Lx7IAE")
        self.assertEqual(billing_line.name, "BL-000320965")
        self.assertEqual(billing_line.project_id, "a003X000015kaPxQAI")
        self.assertEqual(billing_line.currency, "EUR")
        self.assertEqual(
            billing_line.created_date, "2023-05-13T09:04:20.000+0000"
        )
        self.assertEqual(
            billing_line.last_modified_date, "2023-05-13T09:04:20.000+0000"
        )
        self.assertEqual(billing_line.billing_amount, 90.0)
        self.assertEqual(billing_line.billing_date, "2023-05-13")
        self.assertEqual(billing_line.billing_period_ending_date, "2023-05-27")
        self.assertEqual(
            billing_line.billing_period_starting_date, "2023-05-13"
        )
        self.assertEqual(billing_line.hourly_price, None)
        self.assertEqual(billing_line.revenue_dedication, None)
        self.assertEqual(billing_line.billing_plan_amount, "90")
        self.assertEqual(billing_line.billing_plan_billing_date, "2023-05-13")
        self.assertEqual(billing_line.billing_plan_item, "12345")
        self.assertEqual(
            billing_line.billing_plan_service_end_date, "2023-05-27"
        )
        self.assertEqual(
            billing_line.billing_plan_service_start_date, "2023-05-13"
        )

        mock_make_request.assert_called()

    @patch(
        "ms_salesforce_api.salesforce.project.SalesforceQueryExecutor.authenticate"  # noqa: E501
    )
    @patch.object(Project, "fetch_data", side_effect=mock_fetch_data)
    def test_get_opportunities(self, mock_make_request, mock_authenticate):
        mock_authenticate.return_value = "access_token"

        client_id = "client_id"
        username = "username"
        domain = "https://auth.example.com"
        private_key = "private_key"

        project = Project(
            client_id,
            username,
            domain,
            private_key,
            audience="https://login.salesforce.com",
        )
        opportunities = project.get_opportunities()
        self.assertEqual(len(opportunities), 1)

        opportunity = opportunities[0]
        self.assertIsInstance(opportunity, dict)
        self.assertEqual(
            opportunity["client_fiscal_name"],
            "ESMProjectAcc",
        )
        self.assertEqual(
            opportunity["client_account_name"], "ESMProjectAccount"
        )
        self.assertEqual(opportunity["currency"], "EUR")
        self.assertEqual(opportunity["amount"], 0)
        self.assertEqual(opportunity["invoicing_country_code"], "ES")
        self.assertEqual(
            opportunity["operation_coordinator_email"],
            "jhon.doe@ext.makingscience.com",
        )
        self.assertEqual(
            opportunity["operation_coordinator_sub_email"],
            "jhon.doe@ext.makingscience.com",
        )
        self.assertEqual(
            opportunity["created_at"], "2020-07-14T12:55:56.000+0000"
        )
        self.assertEqual(
            opportunity["last_updated_at"], "2023-05-16T13:18:04.000+0000"
        )
        self.assertEqual(opportunity["opportunity_name"], "ESMOPP")
        self.assertEqual(opportunity["stage"], "Qualification")
        self.assertEqual(opportunity["account_billing_country"], "ES")
        self.assertEqual(opportunity["lead_source"], "Other")
        self.assertEqual(opportunity["project_code"], "ESMSEX00430")
        self.assertEqual(opportunity["project_id"], "a003X000015kaPxQAI")
        self.assertEqual(opportunity["project_name"], "ESMProject")
        self.assertEqual(opportunity["project_start_date"], "2023-05-13")
        self.assertEqual(
            opportunity["controller_email"], "jhon.doe@ext.makingscience.com"
        )
        self.assertEqual(
            opportunity["controller_sub_email"],
            "jhon.doe@ext.makingscience.com",
        )
        self.assertIsNone(opportunity["profit_center"])
        self.assertIsNone(opportunity["cost_center"])
        self.assertEqual(opportunity["project_tier"], "Unkown")
        self.assertEqual(
            opportunity["jira_task_url"],
            '<a href="https://makingscience.atlassian.net/browse/ESMSBD0001-11848" target="_blank">View Jira Task</a>',  # noqa: E501
        )
        self.assertEqual(opportunity["opportunity_percentage"], 10.0)
        self.assertEqual(len(opportunity["billing_lines"]), 1)
        billing_line = opportunity["billing_lines"][0]

        self.assertEqual(billing_line["id"], "a0sAa0000004Lx7IAE")
        self.assertEqual(billing_line["name"], "BL-000320965")
        self.assertEqual(billing_line["project_id"], "a003X000015kaPxQAI")
        self.assertEqual(billing_line["currency"], "EUR")
        self.assertEqual(
            billing_line["created_date"], "2023-05-13T09:04:20.000+0000"
        )
        self.assertEqual(
            billing_line["last_modified_date"], "2023-05-13T09:04:20.000+0000"
        )
        self.assertEqual(billing_line["billing_amount"], 90.0)
        self.assertEqual(billing_line["billing_date"], "2023-05-13")
        self.assertEqual(
            billing_line["billing_period_ending_date"], "2023-05-27"
        )
        self.assertEqual(
            billing_line["billing_period_starting_date"], "2023-05-13"
        )
        self.assertEqual(billing_line["hourly_price"], None)
        self.assertEqual(billing_line["revenue_dedication"], None)
        self.assertEqual(billing_line["billing_plan_amount"], "90")
        self.assertEqual(
            billing_line["billing_plan_billing_date"], "2023-05-13"
        )
        self.assertEqual(billing_line["billing_plan_item"], "12345")
        self.assertEqual(
            billing_line["billing_plan_service_end_date"], "2023-05-27"
        )
        self.assertEqual(
            billing_line["billing_plan_service_start_date"], "2023-05-13"
        )

        mock_make_request.assert_called()

    @patch(
        "ms_salesforce_api.salesforce.project.SalesforceQueryExecutor.authenticate"  # noqa: E501
    )
    @patch(
        "ms_salesforce_api.salesforce.project.SalesforceQueryExecutor._make_request"  # noqa: E501
    )
    def test_get_opportunities_empty_on_failure(
        self, mock_make_request, mock_authenticate
    ):
        mock_authenticate.return_value = "access_token"
        mock_make_request.return_value = None

        client_id = "client_id"
        username = "username"
        domain = "https://auth.example.com"
        private_key = "private_key"

        project = Project(
            client_id,
            username,
            domain,
            private_key,
            audience="https://login.salesforce.com",
        )
        query = "SELECT * FROM Opportunity"

        opportunities = project.get_opportunities(query=query)
        self.assertEqual(opportunities, [])

        mock_make_request.assert_called()
