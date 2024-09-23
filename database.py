import oracledb
import os
from dotenv import load_dotenv
from jinja2 import Template
from typing import List
from model import Oportunidade

load_dotenv()


def get_db_credentials(user_env_var: str, password_env_var: str, dsn_env_var: str):
    """
    Retrieve database credentials from environment variables.

    :return: Tuple containing user, password, and dsn
    """
    user = os.getenv(user_env_var)
    password = os.getenv(password_env_var)
    dsn = os.getenv(dsn_env_var)
    return user, password, dsn

def create_oracle_connection(user, password, dsn):
    """
    Create a connection to the Oracle database.

    :param user: Database user
    :param password: Database password
    :param dsn: Data Source Name
    :return: Connection object
    """
    try:
        # Example DSN: "hostname:port/service_name"
        connection = oracledb.connect(user=user, password=password, dsn=dsn)
        print("Successfully connected to Oracle Database")
        return connection
    except oracledb.Error as e:
        print(f"Error connecting to Oracle Database: {e}")
        return None

def execute_query(connection, query, params=None):
    try:
        cursor = connection.cursor()
        cursor.execute(query, params or {})
        cursor.rowfactory = lambda *args: dict(zip([str.lower(d[0]) for d in cursor.description], args))
        results = cursor.fetchall()
        cursor.close()
        return results
    except oracledb.Error as e:
        print(f"Error executing query: {e}")
        return None




def read_query_from_file(file_path: str, **kwargs) -> str:
    """
    Read a SQL query from a file and render it using Jinja2.

    :param file_path: Path to the SQL file
    :param kwargs: Parameters to be passed to the Jinja2 template
    :return: Rendered SQL query as a string
    """
    with open(file_path, 'r') as file:
        template = Template(file.read())
    return template.render(**kwargs)

def get_oportunidades_dcaf(data_inicial: str, data_final: str) -> List[Oportunidade]:
    """
    Retrieve oportunidades from DCAF using the provided date range.

    :param data_inicial: Start date for the query
    :param data_final: End date for the query
    :return: List of oportunidades
    """
    user, password, dsn = get_db_credentials('DCAF_USER', 'DCAF_PASSWORD', 'DCAF_DSN')
    connection = create_oracle_connection(user, password, dsn)
    
    if connection:
        query = read_query_from_file('dcaf.sql', data_inicial=data_inicial, data_final=data_final)
        results = execute_query(connection, query)
        connection.close()
        return [Oportunidade(**r) for r in results]
    return None

# Example usage:
# user, password, dsn = get_db_credentials()
# connection1 = create_oracle_connection(user, password, dsn)
