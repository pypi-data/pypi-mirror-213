from urllib.parse import quote

from gc_google_services_api.bigquery import BigQueryManager


class BigQueryExporter:
    def __init__(self, project_id, dataset_id):
        self.project_id = project_id
        self.dataset_id = dataset_id
        self.client = BigQueryManager(
            project_id=project_id, dataset_id=dataset_id
        )
        self.batch_size = 200
        self.schemas = {
            "opportunities": {
                "currency": "STRING",
                "amount": "FLOAT",
                "invoicing_country_code": "STRING",
                "operation_coordinator_email": "STRING",
                "operation_coordinator_sub_email": "STRING",
                "created_at": "TIMESTAMP",
                "last_updated_at": "TIMESTAMP",
                "opportunity_name": "STRING",
                "stage": "STRING",
                "lead_source": "STRING",
                "project_code": "STRING",
                "project_id": "STRING",
                "project_name": "STRING",
                "project_start_date": "DATE",
                "controller_email": "STRING",
                "controller_sub_email": "STRING",
                "profit_center": "STRING",
                "cost_center": "STRING",
                "project_tier": "STRING",
                "jira_task_url": "STRING",
                "opportunity_percentage": "STRING",
            },
            "billing_lines": {
                "id": "STRING",
                "project_id": "STRING",
                "name": "STRING",
                "currency": "STRING",
                "created_date": "TIMESTAMP",
                "last_modified_date": "TIMESTAMP",
                "billing_amount": "FLOAT",
                "billing_date": "DATE",
                "billing_period_ending_date": "DATE",
                "billing_period_starting_date": "DATE",
                "hourly_price": "FLOAT",
                "revenue_dedication": "FLOAT",
                "billing_plan_amount": "STRING",
                "billing_plan_billing_date": "DATE",
                "billing_plan_item": "STRING",
                "billing_plan_service_end_date": "DATE",
                "billing_plan_service_start_date": "DATE",
            },
            "project_line_items": {
                "country": "STRING",
                "project_id": "STRING",
                "created_date": "TIMESTAMP",
                "effort": "STRING",
                "ending_date": "DATE",
                "id": "STRING",
                "last_modified_date": "TIMESTAMP",
                "ms_pli_name": "STRING",
                "product_name": "STRING",
                "quantity": "FLOAT",
                "starting_date": "DATE",
                "total_price": "STRING",
                "unit_price": "STRING",
            },
            "accounts": {
                "id": "STRING",
                "project_id": "STRING",
                "name": "STRING",
                "account_assigment_group": "STRING",
                "tax_category": "STRING",
                "tax_classification": "STRING",
                "sap_id": "STRING",
                "business_function": "STRING",
                "tax_id_type": "STRING",
                "currency_code": "STRING",
                "created_date": "STRING",
                "tier": "STRING",
                "pec_email": "STRING",
                "phone": "STRING",
                "fax": "STRING",
                "website": "STRING",
                "cif": "STRING",
                "billing_country_code": "STRING",
                "business_name": "STRING",
                "billing_address": "STRING",
                "billing_city": "STRING",
                "billing_postal_code": "STRING",
                "billing_street": "STRING",
                "company_invoicing": "STRING",
                "office": "STRING",
                "payment_terms": "STRING",
                "billing_state_sode": "STRING",
                "mail_invoicing": "STRING",
                "invoicing_email": "STRING",
            },
        }

        for table_name, table_schema in self.schemas.items():
            self.client.create_table_if_not_exists(table_name, table_schema)

    def _export_opportunities(self, opportunities):
        opportunities_values = []
        for opp in opportunities:
            project_start_date = (
                f'DATE "{opp["project_start_date"]}"'
                if opp["project_start_date"]
                else "NULL"
            )
            profit_center = (
                f'"{opp["profit_center"]}"' if opp["profit_center"] else "NULL"
            )
            cost_center = (
                f'"{opp["cost_center"]}"' if opp["cost_center"] else "NULL"
            )

            opportunities_values.append(
                f"""
                (
                    "{opp['currency']}",
                    {opp['amount']},
                    "{opp['invoicing_country_code']}",
                    "{opp['operation_coordinator_email']}",
                    "{opp['operation_coordinator_sub_email']}",
                    TIMESTAMP "{opp['created_at']}",
                    TIMESTAMP "{opp['last_updated_at']}",
                    "{opp['opportunity_name']}",
                    "{opp['stage']}",
                    "{opp['lead_source']}",
                    "{opp['project_code']}",
                    "{opp['project_id']}",
                    "{opp['project_name']}",
                    {project_start_date},
                    "{opp['controller_email']}",
                    "{opp['controller_sub_email']}",
                    {profit_center},
                    {cost_center},
                    "{opp['project_tier']}",
                    "{quote(opp['jira_task_url'], safe='s')}",
                   "{opp['opportunity_percentage']}"
                )
                """
            )
        if opportunities_values:
            insert_opportunities_query = f"""
                INSERT INTO `{self.project_id}.{self.dataset_id}.opportunities` (
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
                ) VALUES {', '.join(opportunities_values)};
            """
            self.client.execute_query(insert_opportunities_query, None)

    def _export_billing_lines(self, opportunities):
        billing_lines_values = []
        for opp in opportunities:
            for bl in opp["billing_lines"]:
                billing_date = (
                    f'DATE "{bl["billing_date"]}"'
                    if bl["billing_date"]
                    else "NULL"
                )
                billing_period_ending_date = (
                    f'DATE "{bl["billing_period_ending_date"]}"'
                    if bl["billing_period_ending_date"]
                    else "NULL"
                )
                billing_period_starting_date = (
                    f'DATE "{bl["billing_period_starting_date"]}"'
                    if bl["billing_period_starting_date"]
                    else "NULL"
                )
                billing_plan_billing_date = (
                    f'DATE "{bl["billing_plan_billing_date"]}"'
                    if bl["billing_plan_billing_date"]
                    else "NULL"
                )
                billing_plan_service_end_date = (
                    f'DATE "{bl["billing_plan_service_end_date"]}"'
                    if bl["billing_plan_service_end_date"]
                    else "NULL"
                )
                billing_plan_service_start_date = (
                    f'DATE "{bl["billing_plan_service_start_date"]}"'
                    if bl["billing_plan_service_start_date"]
                    else "NULL"
                )

                billing_lines_values.append(
                    f"""
                    (
                        "{bl['id']}",
                        "{bl['project_id']}",
                        "{bl['name']}",
                        "{bl['currency']}",
                        TIMESTAMP "{bl['created_date']}",
                        TIMESTAMP "{bl['last_modified_date']}",
                        {bl['billing_amount']},
                        {billing_date},
                        {billing_period_ending_date},
                        {billing_period_starting_date},
                        {bl['hourly_price'] if bl['hourly_price'] else 'NULL'},
                        {bl['revenue_dedication'] if bl['revenue_dedication'] else 'NULL'},
                        "{bl['billing_plan_amount']}",
                        {billing_plan_billing_date},
                        "{bl['billing_plan_item']}",
                        {billing_plan_service_end_date},
                        {billing_plan_service_start_date}
                    )
                    """
                )
        if billing_lines_values:
            insert_billing_lines_query = f"""
                INSERT INTO `{self.project_id}.{self.dataset_id}.billing_lines` (
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
                ) VALUES {', '.join(billing_lines_values)};
            """

            self.client.execute_query(insert_billing_lines_query, None)

    def _export_PLIs(self, opportunities):
        project_line_items_values = []
        for opp in opportunities:
            project_id = opp["project_id"]
            for pli in opp["project_line_items"]:
                effort = f"{pli['effort']}" if pli["effort"] else "NULL"
                total_price = (
                    f"{pli['total_price']}" if pli["total_price"] else "NULL"
                )
                unit_price = (
                    f"{pli['unit_price']}" if pli["unit_price"] else "NULL"
                )
                ending_date = (
                    f'DATE "{pli["ending_date"]}"'
                    if pli["ending_date"]
                    else "NULL"
                )
                starting_date = (
                    f'DATE "{pli["starting_date"]}"'
                    if pli["starting_date"]
                    else "NULL"
                )

                project_line_items_values.append(
                    f"""
                    (
                        "{pli['country']}",
                        TIMESTAMP "{pli['created_date']}",
                        "{effort}",
                        {ending_date},
                        "{pli['id']}",
                        TIMESTAMP "{pli['last_modified_date']}",
                        "{pli['ms_pli_name']}",
                        "{pli['product_name']}",
                        {pli['quantity'] if pli['quantity'] else 0.0},
                        {starting_date},
                        "{total_price}",
                        "{unit_price}",
                        "{project_id}"
                    )
                    """
                )

        if project_line_items_values:
            insert_project_line_items_query = f"""
                INSERT INTO `{self.project_id}.{self.dataset_id}.project_line_items` (
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
                ) VALUES {', '.join(project_line_items_values)};
            """
            self.client.execute_query(insert_project_line_items_query, None)

    def _export_accounts(self, opportunities):
        account_values = []
        for opp in opportunities:
            client_account_name = (
                f'"{opp["client_account_name"]}"'
                if opp["client_account_name"]
                else "NULL"
            )
            account_assigment_group = (
                f'"{opp["account_assigment_group"]}"'
                if opp["account_assigment_group"]
                else "NULL"
            )
            account_tax_category = (
                f'"{opp["account_tax_category"]}"'
                if opp["account_tax_category"]
                else "NULL"
            )
            account_tax_classification = (
                f'"{opp["account_tax_classification"]}"'
                if opp["account_tax_classification"]
                else "NULL"
            )
            account_txt_sapid = (
                f'"{opp["account_txt_sapid"]}"'
                if opp["account_txt_sapid"]
                else "NULL"
            )
            account_business_function = (
                f'"{opp["account_business_function"]}"'
                if opp["account_business_function"]
                else "NULL"
            )
            account_tax_id_type = (
                f'"{opp["account_tax_id_type"]}"'
                if opp["account_tax_id_type"]
                else "NULL"
            )
            account_currency_code = (
                f'"{opp["account_currency_code"]}"'
                if opp["account_currency_code"]
                else "NULL"
            )
            account_created_date = (
                f'"{opp["account_created_date"]}"'
                if opp["account_created_date"]
                else "NULL"
            )
            account_tier = (
                f'"{opp["account_tier"]}"' if opp["account_tier"] else "NULL"
            )
            account_pec_email = (
                f'"{opp["account_pec_email"]}"'
                if opp["account_pec_email"]
                else "NULL"
            )
            account_phone = (
                f'"{opp["account_phone"]}"' if opp["account_phone"] else "NULL"
            )
            account_fax = (
                f'"{opp["account_fax"]}"' if opp["account_fax"] else "NULL"
            )
            account_website = (
                f'"{opp["account_website"]}"'
                if opp["account_website"]
                else "NULL"
            )
            account_cif = (
                f'"{opp["account_cif"]}"' if opp["account_cif"] else "NULL"
            )
            account_billing_country = (
                f'"{opp["account_billing_country"]}"'
                if opp["account_billing_country"]
                else "NULL"
            )
            client_fiscal_name = (
                f'"{opp["client_fiscal_name"]}"'
                if opp["client_fiscal_name"]
                else "NULL"
            )
            account_billing_address = (
                f'"{opp["account_billing_address"]}"'
                if opp["account_billing_address"]
                else "NULL"
            )
            account_billing_city = (
                f'"{opp["account_billing_city"]}"'
                if opp["account_billing_city"]
                else "NULL"
            )
            account_billing_postal_code = (
                f'"{opp["account_billing_postal_code"]}"'
                if opp["account_billing_postal_code"]
                else "NULL"
            )
            account_billing_street = (
                f'"{opp["account_billing_street"]}"'
                if opp["account_billing_street"]
                else "NULL"
            )
            account_company_invoicing = (
                f'"{opp["account_company_invoicing"]}"'
                if opp["account_company_invoicing"]
                else "NULL"
            )
            account_office = (
                f'"{opp["account_office"]}"'
                if opp["account_office"]
                else "NULL"
            )
            account_payment_terms = (
                f'"{opp["account_payment_terms"]}"'
                if opp["account_payment_terms"]
                else "NULL"
            )
            account_billing_state_code = (
                f'"{opp["account_billing_state_code"]}"'
                if opp["account_billing_state_code"]
                else "NULL"
            )
            account_mail_invoicing = (
                f'"{opp["account_mail_invoicing"]}"'
                if opp["account_mail_invoicing"]
                else "NULL"
            )
            account_invoicing_email = (
                f'"{opp["account_invoicing_email"]}"'
                if opp["account_invoicing_email"]
                else "NULL"
            )

            account_values.append(
                f"""
                (
                    "{opp['project_id']}",
                    {client_account_name},
                    {account_assigment_group},
                    {account_tax_category},
                    {account_tax_classification},
                    {account_txt_sapid},
                    {account_business_function},
                    {account_tax_id_type},
                    {account_currency_code},
                    {account_created_date},
                    {account_tier},
                    {account_pec_email},
                    {account_phone},
                    {account_fax},
                    {account_website},
                    {account_cif},
                    {account_billing_country},
                    {client_fiscal_name},
                    {account_billing_address},
                    {account_billing_city},
                    {account_billing_postal_code},
                    {account_billing_street},
                    {account_company_invoicing},
                    {account_office},
                    {account_payment_terms},
                    {account_billing_state_code},
                    {account_mail_invoicing},
                    {account_invoicing_email}
                )
                """
            )
        if account_values:
            insert_opportunities_query = f"""
                INSERT INTO `{self.project_id}.{self.dataset_id}.accounts` (
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
                ) VALUES {', '.join(account_values)};
            """
            self.client.execute_query(insert_opportunities_query, None)

    def export_data(self, opportunities):
        opportunities_batches = [
            opportunities[i : i + self.batch_size]  # noqa: E203
            for i in range(0, len(opportunities), self.batch_size)
        ]
        for batch in opportunities_batches:
            self._export_opportunities(batch)

            self._export_billing_lines(batch)

            self._export_PLIs(batch)

            self._export_accounts(batch)
