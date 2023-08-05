# How to contribute
After clone repository

## 1.- Install dependencies
```bash
poetry install
```

## 2.- Run test
```bash
make test
```

## 3.- Run lint
```bash
make lint && make isort
```

## How to publish new version
Once we have done a merge of our Pull request and we have the updated master branch we can generate a new version. For them we have 3 commands that change the version of our library and generate the corresponding tag so that the Bitbucket pipeline starts and publishes our library automatically.

```bash
make release-patch
```

```bash
make release-minor
```

```bash
make release-major
```

# How works
This project provides an API for querying Salesforce opportunities data and transforming it into an easy-to-use format. The API is built upon the `SalesforceQueryExecutor` and `Project` classes, with the latter inheriting from `SalesforceQueryExecutor`.

## Installation

Make sure you have **Python 3.8+** installed. Then, install the required dependencies using `poetry`:

```bash
poetry install
```

## Usage

First, import the necessary classes:

```python
from ms_salesforce_api.salesforce.project import Project
```

Then, initialize the `Project` class with your Salesforce credentials:

```python
project = Project(
    client_id="your_client_id",
    username="your_username",
    domain="your_domain",
    private_key="your_private_key",
    audience="https://login.salesforce.com", # Default value
    session_duration_hours=1, # Default value
    api_version='57.0',  # Default value
)
```

Now, you can call the get_opportunities method with a query to get the opportunities data:

```python
opportunities = project.get_opportunities()
```

The opportunities variable will contain an array of opportunity objects with the transformed data. For example:

```python
{
    "success": true,
    "opportunities": [
        {
            "client_fiscal_name": "ESMProjectAcc",
            "client_account_name": "ESMProjectAccount",
            "currency": "EUR",
            "amount": 0,
            "invoicing_country_code": "ES",
            "operation_coordinator_email": "jhon.doe@ext.makingscience.com",
            "operation_coordinator_sub_email": "jhon.doe@ext.makingscience.com",
            "created_at": "2020-07-14T12:55:56.000+0000",
            "last_updated_at": "2023-05-16T13:18:04.000+0000",
            "opportunity_name": "ESMOPP",
            "stage": "Qualification",
            "billing_country": "ES",
            "lead_source": "Other",
            "project_code": "ESMSEX00430",
            "project_id": "a003X000015kaPxQAI",
            "project_name": "ESMProject",
            "project_start_date": "2023-05-13",
            "controller_email": "jhon.doe@ext.makingscience.com",
            "controller_sub_email": "jhon.doe@ext.makingscience.com",
            "profit_center": None,
            "cost_center": None,
            "project_tier": "Unkown",
            "jira_task_url": "<a href=\"https://makingscience.atlassian.net/browse/ESMSBD0001-11848\" target=\"_blank\">View Jira Task</a>",
            "opportunity_percentage": 10.0,
            "billing_lines": [
                {
                    "id": "a0sAa0000004Lx7IAE",
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
                    "billing_plan_service_start_date": "2023-05-13"
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
                    "unit_price": 90.0
                }
            ]
        }
    ]
}
```

You can customize the query as needed to retrieve different data from Salesforce.

```python
query = "SELECT Id, Name FROM Project WHERE Project.Id = 'ESMS0000'"

opportunities = project.get_opportunities(query=query)
```

# How the information retrieval works

This service retrieves the information in two steps:

First, it makes a query to the Salesforce API to get a list of project opportunities.

Then, for each opportunity, it makes a concurrent request to the Salesforce API to get its billing lines.
In the end, it merges the opportunity information with their respective billing lines and returns a dictionary with all the data.

# Testing
To run the unit tests, simply execute the following command:

```bash
make test
```
This will run all the tests and display the results. Make sure that all tests pass before using the API in a production environment.
