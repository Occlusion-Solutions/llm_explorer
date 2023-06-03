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
            "telemetry": "explorer/sql/ddl_tse_telemetry.sql",
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


# class Snowddl:
#     '''
#     Snowddl class loads DDL files for various tables in a database.

#     Attributes:
#         ddl_dict (dict): dictionary of DDL files for various tables in a database.

#     Methods:
#         load_ddls: loads DDL files for various tables in a database.
#     '''
#     def __init__(self):
#         self.ddl_dict = self.load_ddls()
#         self._conn = snowflake.connector.connect(
#             user=st.secrets.connections.snowflake.user,
#             password=st.secrets.connections.snowflake.password,
#             account=st.secrets.connections.snowflake.account,
#             warehouse=st.secrets.connections.snowflake.warehouse,
#             role=st.secrets.connections.snowflake.role,
#             database=st.secrets.connections.snowflake.database,
#             schema=st.secrets.connections.snowflake.schema,
#         )

#     @staticmethod
#     def load_ddls():
#         ddl_files = {
#             "telemetry": "sql/ddl_tse_telemetry.sql",
#         }

#         ddl_dict = {}
#         for table_name, file_name in ddl_files.items():
#             with open(file_name, "r") as f:
#                 ddl_dict[table_name] = f.read()
#         return ddl_dict


#     # function - run sql query and return data
#     def query_data_warehouse(self, sql: str, parameters=None) -> any:
#         """
#         Executes snowflake sql query and returns result as data as dataframe.
#         Example of parameters
#         :param sql: sql query to be executed
#         :param parameters: named parameters used in the sql query (defaulted as None)
#         :return: dataframe
#         """
#         if parameters is None:
#             parameters = {}
#         query = sql
#         # Create a cursor object.
#         #cur = self._conn.cursor()

#         try:
#             # cur.execute("USE DATABASE " + st.secrets.connections.snowflake.database)
#             # cur.execute("USE SCHEMA " + st.secrets.connections.snowflake.schema)
#             # cur.execute(query, parameters)
#             # all_rows = cur.fetchall()
#             # field_names = [i[0] for i in cur.description]
#             ...

#         except Exception as e:
#             return e

#         finally:
#             print("closing cursor")

#         #df = pd.DataFrame(all_rows)
#         #df.columns = field_names
#         return None #df#


#     def generate_df(to_extract: str):
#         '''
#         Generate a dataframe from the query by querying the data warehouse.

#         Args:
#             to_extract (str): The query

#         Returns:
#             df (pandas.DataFrame): The dataframe generated from the query

#         '''
#         df = snow_ddl.query_data_warehouse(to_extract)
#         st.dataframe(df, use_container_width=True)
