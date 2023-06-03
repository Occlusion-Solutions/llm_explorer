import pandas as pd

# import snowflake.connector
import streamlit as st
from databricks import sql as adb_sql


class ADBDDL:
    """
    ADBDDL class loads DDL files for various tables in a database for Databricks and Delta Lake.
    """

    def __init__(self):
        self.ddl_dict = self.load_ddls()

    @staticmethod
    def load_ddls():
        ddl_files = {
            "telemetry": "llm_explorer/sql/ddl_tse_telemetry.sql",
        }

        ddl_dict = {}
        for table_name, file_name in ddl_files.items():
            with open(file_name, "r") as f:
                ddl_dict[table_name] = f.read()
        return ddl_dict

    def query_lakehouse(self, query) -> pd.DataFrame:
        """
        Executes databricks sql query and returns result as data as dataframe.
        Example of parameters
        :param sql: sql query to be executed
        """
        print(f"Received query: {query}")
        try:
            with adb_sql.connect(
                server_hostname=st.secrets.connections.databricks.server_hostname,
                http_path=st.secrets.connections.databricks.http_path,
                access_token=st.secrets.connections.databricks.access_token,
            ) as adb_connection:
                try:
                    with adb_connection.cursor() as cursor:
                        print(f"Opened cursor {cursor}")
                        cursor.execute(query)
                        column_names = [desc[0] for desc in cursor.description]
                        data = cursor.fetchall()
                        print(data)
                        df = pd.DataFrame(data, columns=column_names)
                        return df
                except Exception as e:
                    print(f"Error in cursor {e}")
        except Exception as e:
            print(f"Error in connection {e}")
