import logging

import psycopg2
from psycopg2 import sql

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class CloudSQL:
    BATCH_SIZE = 200

    def __init__(self, host, user, password, dbname, debug_mode=False):
        self.debug_mode = debug_mode

        self.check_and_create_database(host, user, password, dbname)

        self.connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            dbname=dbname,
        )

    def check_and_create_database(self, host, user, password, database):
        conn = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            dbname="postgres",
        )

        cursor = conn.cursor()

        check_db_query = f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{database}'"  # noqa: E501

        cursor.execute(check_db_query)

        result = cursor.fetchone()

        if result is None:
            logging.info(f"Creating database '{database}'...")
            create_db_query = f"CREATE DATABASE {database}"
            cursor.execute("COMMIT")
            cursor.execute(create_db_query)
            logging.info(f"Database '{database}' created.")

        conn.commit()

        cursor.close()
        conn.close()

    def export_data(self, opportunities):
        with self.connection.cursor() as cursor:
            opportunity_batches = self._create_batches(
                opportunities, self.BATCH_SIZE
            )
            for opportunity_batch in opportunity_batches:
                self._insert_opportunities_batch(cursor, opportunity_batch)

                billing_lines = []
                project_lines = []

                for opportunity in opportunity_batch:
                    billing_lines.extend(
                        self._create_billing_lines(
                            opportunity.get("billing_lines", []),
                            opportunity["project_id"],
                        )
                    )

                    project_lines.extend(
                        self._create_project_lines(
                            opportunity.get("project_line_items", []),
                            opportunity["project_id"],
                        )
                    )
                if billing_lines:
                    self._insert_billing_lines_batch(cursor, billing_lines)

                if project_lines:
                    self._insert_project_lines_batch(cursor, project_lines)

        self.connection.commit()

    def _create_batches(self, data, batch_size):
        return [
            data[i : i + batch_size]  # noqa: E203
            for i in range(0, len(data), batch_size)
        ]

    def _create_billing_lines(self, billing_lines, project_id):
        for billing_line in billing_lines:
            billing_line["project_id"] = project_id
        return billing_lines

    def _create_project_lines(self, project_lines, project_id):
        for project_line in project_lines:
            project_line["project_id"] = project_id
        return project_lines

    def _insert_opportunities_batch(self, cursor, opportunities):
        opportunity_fixed = [
            {
                key: (value if value != "" else None)
                for key, value in opportunity.items()
                if key not in ["billing_lines", "project_line_items"]
            }
            for opportunity in opportunities
        ]

        insert_query = sql.SQL(
            """
            INSERT INTO Opportunities ({})
            VALUES ({})
            """
        ).format(
            sql.SQL(", ").join(
                map(sql.Identifier, opportunity_fixed[0].keys())
            ),
            sql.SQL(", ").join(
                map(sql.Placeholder, opportunity_fixed[0].keys())
            ),
        )

        try:
            cursor.executemany(insert_query, opportunity_fixed)
        except Exception as e:
            if self.debug_mode:
                insert_query_string = cursor.mogrify(
                    insert_query.as_string(cursor.connection),
                    opportunity_fixed,
                ).decode("utf-8")
                logging.info(insert_query_string)
            logging.error(
                f"[ERROR - _insert_opportunities_batch (cloudsql)] - {e}"
            )

    def _insert_billing_lines_batch(self, cursor, billing_lines):
        insert_query = sql.SQL(
            """
            INSERT INTO BillingLines ({})
            VALUES ({})
        """
        ).format(
            sql.SQL(", ").join(map(sql.Identifier, billing_lines[0].keys())),
            sql.SQL(", ").join(map(sql.Placeholder, billing_lines[0].keys())),
        )

        try:
            cursor.executemany(insert_query, billing_lines)
        except Exception as e:
            if self.debug_mode:
                insert_query_string = cursor.mogrify(
                    cursor.query, billing_lines
                ).decode("utf-8")
                logging.info(insert_query_string)
            logging.error(
                f"[ERROR - _insert_billing_lines_batch (cloudsql)] - {e}"
            )

    def _insert_project_lines_batch(self, cursor, project_lines):
        insert_query = sql.SQL(
            """
            INSERT INTO ProjectLine ({})
            VALUES ({})
        """
        ).format(
            sql.SQL(", ").join(map(sql.Identifier, project_lines[0].keys())),
            sql.SQL(", ").join(map(sql.Placeholder, project_lines[0].keys())),
        )

        try:
            cursor.executemany(insert_query, project_lines)
        except Exception as e:
            if self.debug_mode:
                insert_query_string = cursor.mogrify(
                    cursor.query, project_lines
                ).decode("utf-8")
                logging.info(insert_query_string)
            logging.error(
                f"[ERROR - _insert_project_lines_batch (cloudsql)] - {e}"
            )
