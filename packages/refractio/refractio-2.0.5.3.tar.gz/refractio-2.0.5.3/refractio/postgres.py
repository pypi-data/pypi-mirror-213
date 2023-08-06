#! -*- coding: utf-8 -*-
"""Class to get postgres connection object and related operations"""

import os
import pandas.io.sql as sqlio
from .manager import (
    get_conn_details_from_conn_name,
    get_conn_details_from_ds_name,
    validate_project_id,
    default_connection_name,
    get_dataframe_query
)


class Postgres:

    def __init__(self):
        self.__connection_details = None
        self.con_obj = None

    def _get_connection(self):
        try:
            # Connect to Postgres
            import psycopg2
            self.con_obj = psycopg2.connect(
                # todo: To update the keys here, once we have the connection manager API created for refractio.
                user=self.__connection_details["params"]["READER"].get("user") if self.__connection_details["params"]["READER"].get("user") else self.__connection_details["params"]["READER"].get("dbUserName"),
                password=self.__connection_details["params"]["READER"].get("password") if self.__connection_details["params"]["READER"].get("password") else self.__connection_details["params"]["READER"].get("dbPassword"),
                host=self.__connection_details["params"]["READER"]["host"] if self.__connection_details["params"]["READER"].get("host") else self.__connection_details["params"]["READER"].get("ipAddress"),
                port=int(self.__connection_details["params"]["READER"]["port"]),
                database=self.__connection_details["params"]["READER"].get("database") if self.__connection_details["params"]["READER"].get("database") else self.__connection_details["params"]["READER"].get("defaultDb")
            )
        except Exception as ex:
            print(f"Connection details fetched: {self.__connection_details}")
            print(f"Ex: {ex}")
            raise Exception(f"Exception occurred in creating postgres connection: "
                            f"{self.__connection_details.get('detailMessage')}")

    def get_connection(self, connection_name=None):
        try:
            # Getting connection
            if self.con_obj is None or self.con_obj.closed:
                # Getting default connection name
                if connection_name is None:
                    connection_name = default_connection_name("POSTGRES")
                    if not connection_name:
                        raise Exception("Could not get the default connection name,"
                                        "please create/pass an active postgres connection name.")
                self.__connection_details = get_conn_details_from_conn_name(
                    connection_name=connection_name, connection_type="postgres")
                self._get_connection()
                print(f"Connection object created: {self.con_obj}\nPlease close the connection after use!")
            else:
                print(f"Existing connection object fetched: {self.con_obj}\nPlease close the connection after use!")

            return self.con_obj
        except Exception as ex:
            print(f"Exception occurred in getting postgres connection: {ex}")

    def get_dataframe(self, dataset_name, project_id=os.getenv("project_id"), row_count=-1, filter_condition=None):
        try:
            project_id = validate_project_id(project_id)

            self.__connection_details = get_conn_details_from_ds_name(dataset_name=dataset_name, project_id=project_id)
            # Creating new connection attached to dataset_id for reading the dataset.
            self._get_connection()

            query = get_dataframe_query(f"{self.__connection_details['params']['READER']['database']}."
                                        f"{self.__connection_details['params']['READER']['tables']}",
                                        row_count, filter_condition)     # Get query to fetch details

            data_frame = sqlio.read_sql_query(query, con=self.con_obj)   # Read data from postgres

            self.con_obj.close()    # Closing the connection used for reading dataset.
            return data_frame
        except Exception as ex:
            print(f"Exception occurred in reading data_frame from postgres connection: {ex}")

    def execute_query(self, query, connection_name=None):
        try:
            # Getting connection object
            if self.con_obj is None or self.con_obj.closed:
                self.get_connection(connection_name)

            data_frame = sqlio.read_sql_query(query, con=self.con_obj)   # Fetch all records in pandas dataframe

            self.con_obj.close()    # Closing the connection
            return data_frame
        except Exception as ex:
            print(f"Exception occurred in execute_query: {ex}")

    def close_connection(self):
        self.con_obj.close()
        print("postgres connection closed!")
