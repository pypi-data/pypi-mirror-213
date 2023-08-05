import re
import unittest
from unittest import mock


class BigQueryExporterTestCase(unittest.TestCase):
    def setUp(self):
        self.project_id = "your-project-id"
        self.dataset_id = "your-dataset-id"

        self.opportunities = [
            {
                "client_fiscal_name": "ESMProjectAcc",
                "client_account_name": "ESMProjectAccount",
                "currency": "EUR",
                "amount": 0,
                "invoicing_country_code": "ES",
                "operation_coordinator_email": "test@test.com",
                "operation_coordinator_sub_email": "test@test.com",
                "created_at": "2020-07-14T12:55:56.000+0000",
                "last_updated_at": "2023-05-16T13:18:04.000+0000",
                "opportunity_name": "ESMOPP",
                "stage": "Qualification",
                "lead_source": "Other",
                "project_code": "ESMSEX00430",
                "project_id": "a003X000015kaPxQAI",
                "project_name": "ESMProject",
                "project_start_date": "2023-05-13",
                "controller_email": "test@test.com",
                "controller_sub_email": "test@test.com",
                "profit_center": None,
                "cost_center": None,
                "project_tier": "Unknown",
                "jira_task_url": "ESMSBD0001-11848",
                "opportunity_percentage": 10.0,
                "billing_lines": [
                    {
                        "id": "a0sAa0000004Lx7IAE",
                        "project_id": "a003X000015kaPxQAI",
                        "name": "BL-000320965",
                        "currency": "EUR",
                        "created_date": "2023-05-13T09:04:20.000+0000",
                        "last_modified_date": "2023-05-16T13:18:01.000+0000",
                        "billing_amount": 90.0,
                        "billing_date": "2023-05-13",
                        "billing_period_ending_date": "2023-05-27",
                        "billing_period_starting_date": "2023-05-13",
                        "hourly_price": None,
                        "revenue_dedication": None,
                        "billing_plan_amount": "90",
                        "billing_plan_billing_date": "2023-05-13",
                        "billing_plan_item": "12345",
                        "billing_plan_service_end_date": "2023-05-27",
                        "billing_plan_service_start_date": "2023-05-13",
                    }
                ],
                "project_line_items": [
                    {
                        "country": "Spain",
                        "created_date": "2023-05-13T09:03:14.000+0000",
                        "effort": "12",
                        "ending_date": "2023-05-27",
                        "id": "a0VAa000000fWbdMAE",
                        "last_modified_date": "2023-05-16T13:18:01.000+0000",
                        "ms_pli_name": "_MSEX00430",
                        "product_name": "ESM PRODUCT",
                        "quantity": 12.0,
                        "starting_date": "2023-05-13",
                        "total_price": 1080.0,
                        "unit_price": 90.0,
                    }
                ],
                "account_billing_country": "ES",
                "account_assigment_group": None,
                "account_tax_category": None,
                "account_tax_classification": "0",
                "account_txt_sapid": "10004171",
                "account_business_function": "BP03",
                "account_tax_id_type": "CA2",
                "account_currency_code": "",
                "account_created_date": "2023-02-15T09:27:46.000+0000",
                "account_tier": "T1",
                "account_pec_email": None,
                "account_phone": None,
                "account_fax": None,
                "account_website": None,
                "account_cif": "700812894RC0001",
                "account_billing_address": "12 Strickland Avenue, Toronto, Ontario, M6K 2H8, Canada",  # noqa: E501
                "account_billing_city": "Toronto",
                "account_billing_postal_code": "M6K 2H8",
                "account_billing_street": "12 Strickland Avenue",
                "account_company_invoicing": "2411",
                "account_office": "1313X000000Y5DEQA0",
                "account_payment_terms": "T060",
                "account_billing_state_code": "ON",
                "account_mail_invoicing": None,
                "account_invoicing_email": "test@5822.group",
            },
        ]

        self.mock_bigquery_manager = mock.patch(
            "gc_google_services_api.bigquery.BigQueryManager"
        ).start()
        from ..Bigquery import BigQueryExporter

        self.exporter = BigQueryExporter(self.project_id, self.dataset_id)

    def tearDown(self):
        self.mock_bigquery_manager.reset_mock()

    def test_export_opportunities(self):
        self.exporter._export_opportunities(self.opportunities)

        expected_query = """
            INSERT INTO `your-project-id.your-dataset-id.opportunities` (
                    currency,
                    amount,
                    invoicing_country_code,
                    operation_coordinator_email,
                    operation_coordinator_sub_email,
                    created_at,
                    last_updated_at,
                    opportunity_name,
                    stage,
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
                    opportunity_percentage
                ) VALUES (
                    "EUR",
                    0,
                    "ES",
                    "test@test.com",
                    "test@test.com",
                    TIMESTAMP "2020-07-14T12:55:56.000+0000",
                    TIMESTAMP "2023-05-16T13:18:04.000+0000",
                    "ESMOPP",
                    "Qualification",
                    "Other",
                    "ESMSEX00430",
                    "a003X000015kaPxQAI",
                    "ESMProject",
                    DATE "2023-05-13",
                    "test@test.com",
                    "test@test.com",
                    NULL,
                    NULL,
                    "Unknown",
                    "ESMSBD0001-11848",
                   "10.0"
                );
        """
        execute_query_calls = self.exporter.client.execute_query.call_args_list

        expected_query_stripped = re.sub(r"\s+", "", expected_query)

        match_found = any(
            expected_query_stripped == re.sub(r"\s+", "", str(call[0][0]))
            for call in execute_query_calls
        )

        self.assertTrue(match_found)

    def test_export_billing_lines(self):
        self.exporter._export_billing_lines(self.opportunities)

        expected_query = """
            INSERT INTO `your-project-id.your-dataset-id.billing_lines` (
                id,
                project_id,
                name,
                currency,
                created_date,
                last_modified_date,
                billing_amount,
                billing_date,
                billing_period_ending_date,
                billing_period_starting_date,
                hourly_price,
                revenue_dedication,
                billing_plan_amount,
                billing_plan_billing_date,
                billing_plan_item,
                billing_plan_service_end_date,
                billing_plan_service_start_date
            ) VALUES (
                "a0sAa0000004Lx7IAE",
                "a003X000015kaPxQAI",
                "BL-000320965",
                "EUR",
                TIMESTAMP "2023-05-13T09:04:20.000+0000",
                TIMESTAMP "2023-05-16T13:18:01.000+0000",
                90.0,
                DATE "2023-05-13",
                DATE "2023-05-27",
                DATE "2023-05-13",
                NULL,
                NULL,
                "90",
                DATE "2023-05-13",
                "12345",
                DATE "2023-05-27",
                DATE "2023-05-13"
            );
        """
        execute_query_calls = self.exporter.client.execute_query.call_args_list

        expected_query_stripped = re.sub(r"\s+", "", expected_query)
        execute_query_stripped = re.sub(
            r"\s+", "", str(execute_query_calls[0][0][0])
        )

        self.assertEqual(execute_query_stripped, expected_query_stripped)

    def test_export_PLIs(self):
        self.exporter._export_PLIs(self.opportunities)

        expected_query = """
            INSERT INTO `your-project-id.your-dataset-id.project_line_items` (
                country,
                created_date,
                effort,
                ending_date,
                id,
                last_modified_date,
                ms_pli_name,
                product_name,
                quantity,
                starting_date,
                total_price,
                unit_price,
                project_id
            ) VALUES (
                "Spain",
                TIMESTAMP "2023-05-13T09:03:14.000+0000",
                "12",
                DATE "2023-05-27",
                "a0VAa000000fWbdMAE",
                TIMESTAMP "2023-05-16T13:18:01.000+0000",
                "_MSEX00430",
                "ESM PRODUCT",
                12.0,
                DATE "2023-05-13",
                "1080.0",
                "90.0",
                "a003X000015kaPxQAI"
            );
        """

        execute_query_calls = self.exporter.client.execute_query.call_args_list

        expected_query_stripped = re.sub(r"\s+", "", expected_query)
        execute_query_stripped = re.sub(
            r"\s+", "", str(execute_query_calls[0][0][0])
        )

        self.assertEqual(execute_query_stripped, expected_query_stripped)

    @mock.patch(
        "ms_salesforce_api.salesforce.project.export_data.Bigquery.BigQueryManager"  # noqa: E501
    )
    def test_export_data(self, mock_bq_manager):
        mock_client = mock.Mock()
        mock_bq_manager.return_value = mock_client

        self.exporter.export_data(self.opportunities)

        expected_opportunities_query = """
            INSERT INTO `your-project-id.your-dataset-id.opportunities` (
                currency,
                amount,
                invoicing_country_code,
                operation_coordinator_email,
                operation_coordinator_sub_email,
                created_at,
                last_updated_at,
                opportunity_name,
                stage,
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
                opportunity_percentage
            ) VALUES (
                "EUR",
                0,
                "ES",
                "test@test.com",
                "test@test.com",
                TIMESTAMP "2020-07-14T12:55:56.000+0000",
                TIMESTAMP "2023-05-16T13:18:04.000+0000",
                "ESMOPP",
                "Qualification",
                "Other",
                "ESMSEX00430",
                "a003X000015kaPxQAI",
                "ESMProject",
                DATE "2023-05-13",
                "test@test.com",
                "test@test.com",
                NULL,
                NULL,
                "Unknown",
                "ESMSBD0001-11848",
                "10.0"
            );
        """

        expected_billing_lines_query = """
            INSERT INTO `your-project-id.your-dataset-id.billing_lines` (
                id,
                project_id,
                name,
                currency,
                created_date,
                last_modified_date,
                billing_amount,
                billing_date,
                billing_period_ending_date,
                billing_period_starting_date,
                hourly_price,
                revenue_dedication,
                billing_plan_amount,
                billing_plan_billing_date,
                billing_plan_item,
                billing_plan_service_end_date,
                billing_plan_service_start_date
            ) VALUES (
                "a0sAa0000004Lx7IAE",
                "a003X000015kaPxQAI",
                "BL-000320965",
                "EUR",
                TIMESTAMP "2023-05-13T09:04:20.000+0000",
                TIMESTAMP "2023-05-16T13:18:01.000+0000",
                90.0,
                DATE "2023-05-13",
                DATE "2023-05-27",
                DATE "2023-05-13",
                NULL,
                NULL,
                "90",
                DATE "2023-05-13",
                "12345",
                DATE "2023-05-27",
                DATE "2023-05-13"
            );
        """

        expected_PLIs_query = """
            INSERT INTO `your-project-id.your-dataset-id.project_line_items` (
                country,
                created_date,
                effort,
                ending_date,
                id,
                last_modified_date,
                ms_pli_name,
                product_name,
                quantity,
                starting_date,
                total_price,
                unit_price,
                project_id
            ) VALUES (
                "Spain",
                TIMESTAMP "2023-05-13T09:03:14.000+0000",
                "12",
                DATE "2023-05-27",
                "a0VAa000000fWbdMAE",
                TIMESTAMP "2023-05-16T13:18:01.000+0000",
                "_MSEX00430",
                "ESM PRODUCT",
                12.0,
                DATE "2023-05-13",
                "1080.0",
                "90.0",
                "a003X000015kaPxQAI"
            );
        """
        expected_accounts_query = """
            INSERT INTO `your-project-id.your-dataset-id.accounts` (
                project_id,
                name,
                account_assigment_group,
                tax_category,
                tax_classification,
                sap_id,
                business_function,
                tax_id_type,
                currency_code,
                created_date,
                tier,
                pec_email,
                phone,
                fax,
                website,
                cif,
                billing_country_code,
                business_name,
                billing_address,
                billing_city,
                billing_postal_code,
                billing_street,
                company_invoicing,
                office,
                payment_terms,
                billing_state_sode,
                mail_invoicing,
                invoicing_email
            ) VALUES
                (
                    "a003X000015kaPxQAI",
                    "ESMProjectAccount",
                    NULL,
                    NULL,
                    "0",
                    "10004171",
                    "BP03",
                    "CA2",
                    NULL,
                    "2023-02-15T09:27:46.000+0000",
                    "T1",
                    NULL,
                    NULL,
                    NULL,
                    NULL,
                    "700812894RC0001",
                    "ES",
                    "ESMProjectAcc",
                    "12 Strickland Avenue, Toronto, Ontario, M6K 2H8, Canada",
                    "Toronto",
                    "M6K 2H8",
                    "12 Strickland Avenue",
                    "2411",
                    "1313X000000Y5DEQA0",
                    "T060",
                    "ON",
                    NULL,
                    "test@5822.group"
                )
                ;
        """
        execute_query_calls = self.exporter.client.execute_query.call_args_list

        expected_opportunities_query_stripped = re.sub(
            r"\s+", "", expected_opportunities_query
        )

        execute_opportunities_query_stripped = re.sub(
            r"\s+", "", str(execute_query_calls[1][0][0])
        )

        expected_billinglines_query_stripped = re.sub(
            r"\s+", "", expected_billing_lines_query
        )

        execute_billinglines_query_stripped = re.sub(
            r"\s+", "", str(execute_query_calls[0][0][0])
        )

        expected_pli_query_stripped = re.sub(r"\s+", "", expected_PLIs_query)
        execute_pli_query_stripped = re.sub(
            r"\s+", "", str(execute_query_calls[3][0][0])
        )

        expected_accounts_query_stripped = re.sub(
            r"\s+", "", expected_accounts_query
        )

        execute_accounts_query_stripped = re.sub(
            r"\s+", "", str(execute_query_calls[4][0][0])
        )

        self.assertEqual(
            execute_opportunities_query_stripped,
            expected_opportunities_query_stripped,
        )

        self.assertEqual(
            execute_billinglines_query_stripped,
            expected_billinglines_query_stripped,
        )

        self.assertEqual(
            execute_pli_query_stripped,
            expected_pli_query_stripped,
        )

        self.assertEqual(
            execute_accounts_query_stripped,
            expected_accounts_query_stripped,
        )
