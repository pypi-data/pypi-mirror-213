#! -*- coding: utf-8 -*-
"""
Class to get SQLSERVER connection object and related operations.
Requirements: This will need sqlserver driver library to work.
To do so,
Create a custom template with the following commands added in init_script section,
sudo curl -o /etc/yum.repos.d/mssql-release.repo https://packages.microsoft.com/config/rhel/9.0/prod.repo
sudo ACCEPT_EULA=Y yum install -y msodbcsql18
"""

import os
import pandas as pd
from .manager import (
    get_conn_details_from_conn_name,
    get_conn_details_from_ds_name,
    validate_project_id,
    default_connection_name,
    get_dataframe_query
)


class Sqlserver:

    def __init__(self):
        self.__connection_details = None
        self.con_obj = None

    def _get_connection(self):
        try:
            # Connect to Sqlserver
            import pyodbc
            # This need the OS should have sql server driver installed. Like,
            # sudo curl -o /etc/yum.repos.d/mssql-release.repo https://packages.microsoft.com/config/rhel/9.0/prod.repo
            # sudo ACCEPT_EULA=Y yum install -y msodbcsql18
            driver_lib = "/opt/microsoft/msodbcsql18/lib64/libmsodbcsql-18.2.so.1.1"    # sqlserver driver lib path
            # todo: To update the keys here, once we have the connection manager API created for refractio.
            if self.__connection_details["params"]["READER"].get("database"):
                connection_string = f'''DRIVER={driver_lib};
                SERVER={self.__connection_details["params"]["READER"]["host"] if self.__connection_details["params"]["READER"].get("host") else self.__connection_details["params"]["READER"].get("ipAddress")};
                UID={self.__connection_details["params"]["READER"].get("user") if self.__connection_details["params"]["READER"].get("user") else self.__connection_details["params"]["READER"].get("dbUserName")};
                PWD={self.__connection_details["params"]["READER"].get("password") if self.__connection_details["params"]["READER"].get("password") else self.__connection_details["params"]["READER"].get("dbPassword")};
                DATABASE={self.__connection_details["params"]["READER"].get("database")};
                TrustServerCertificate=yes;'''
            else:
                connection_string = f'''DRIVER={driver_lib};
                SERVER={self.__connection_details["params"]["READER"]["host"] if self.__connection_details["params"]["READER"].get("host") else self.__connection_details["params"]["READER"].get("ipAddress")};
                UID={self.__connection_details["params"]["READER"].get("user") if self.__connection_details["params"]["READER"].get("user") else self.__connection_details["params"]["READER"].get("dbUserName")};
                PWD={self.__connection_details["params"]["READER"].get("password") if self.__connection_details["params"]["READER"].get("password") else self.__connection_details["params"]["READER"].get("dbPassword")};
                TrustServerCertificate=yes;'''
            self.con_obj = pyodbc.connect(connection_string)
        except Exception as ex:
            print(f"Connection details fetched: {self.__connection_details}")
            print(f"Ex: {ex}")
            raise Exception(f"Exception occurred in creating sql server connection: "
                            f"{self.__connection_details.get('detailMessage')}")

    def get_connection(self, connection_name=None):
        try:
            # Getting connection
            if self.con_obj is None or self.con_obj.closed:
                # Getting default connection name
                if connection_name is None:
                    connection_name = default_connection_name("SQLSERVER")
                    if not connection_name:
                        raise Exception("Could not get the default connection name,"
                                        "please create/pass an active sqlserver connection name.")
                self.__connection_details = get_conn_details_from_conn_name(
                    connection_name=connection_name, connection_type="sqlserver")
                self._get_connection()
                print(f"Connection object created: {self.con_obj}\nPlease close the connection after use!")
            else:
                print(f"Existing connection object fetched: {self.con_obj}\nPlease close the connection after use!")

            return self.con_obj
        except Exception as ex:
            print(f"Exception occurred in getting sqlserver connection: {ex}")

    def get_dataframe(self, dataset_name, project_id=os.getenv("project_id"), row_count=-1, filter_condition=None):
        try:
            project_id = validate_project_id(project_id)

            self.__connection_details = get_conn_details_from_ds_name(dataset_name=dataset_name, project_id=project_id)
            # Creating new connection attached to dataset_id for reading the dataset.
            self._get_connection()

            query = get_dataframe_query(self.__connection_details['params']['READER']['tables'],
                                        row_count, filter_condition, top=True)     # Get query to fetch details

            data_frame = pd.read_sql(query, con=self.con_obj)   # Read data from sqlserver

            self.con_obj.close()    # Closing the connection used for reading dataset.
            return data_frame
        except Exception as ex:
            print(f"Exception occurred in reading data_frame from sqlserver connection: {ex}")

    def execute_query(self, query, database, connection_name=None):
        try:
            # Getting connection object
            if self.con_obj is None or self.con_obj.closed:
                self.get_connection(connection_name)

            if database:
                self.con_obj.execute(f"USE {database}")      # To select database

            data_frame = pd.read_sql(query, con=self.con_obj)   # Fetch all records in pandas dataframe

            self.con_obj.close()    # Closing the connection
            return data_frame
        except Exception as ex:
            print(f"Exception occurred in execute_query: {ex}")

    def close_connection(self):
        self.con_obj.close()
        print("sqlserver connection closed!")
