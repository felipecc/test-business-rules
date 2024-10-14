from contextlib import contextmanager
from typing import Any, Dict, Generator, List, Optional, Tuple, Union
import os
from dotenv import load_dotenv
from jinja2 import Template
from pathlib import Path

# Import both cx_Oracle and oracledb
import cx_Oracle
import oracledb

from model import Oportunidade, Provisionamento, Recebimento, RecebimentoDetalhado

load_dotenv()

def get_db_credentials(user_env_var: str, password_env_var: str, dsn_env_var: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """
    Retrieve database credentials from environment variables.

    :return: Tuple containing user, password, and dsn
    """
    user = os.getenv(user_env_var)
    password = os.getenv(password_env_var)
    dsn = os.getenv(dsn_env_var)
    return user, password, dsn

@contextmanager
def create_cx_oracle_connection(user: str, password: str, dsn: str) -> Generator[cx_Oracle.Connection, None, None]:
    """
    Create a connection to the Oracle database using cx_Oracle.

    :param user: Database user
    :param password: Database password
    :param dsn: Data Source Name
    :return: Connection object
    """
    connection = None
    try:
        connection = cx_Oracle.connect(user=user, password=password, dsn=dsn)
        yield connection
    except cx_Oracle.Error as e:
        print(f"Error connecting to Oracle Database (cx_Oracle): {e}")
        return None
    finally:
        if connection:
            connection.close()

@contextmanager
def create_oracledb_connection(user: str, password: str, dsn: str) -> Generator[oracledb.Connection, None, None]:
    """
    Create a connection to the Oracle database using oracledb.

    :param user: Database user
    :param password: Database password
    :param dsn: Data Source Name
    :return: Connection object
    """
    connection = None
    try:
        connection = oracledb.connect(user=user, password=password, dsn=dsn)
        yield connection
    except oracledb.Error as e:
        print(f"Error connecting to Oracle Database (oracledb): {e}")
        return None
    finally:
        if connection:
            connection.close()

def execute_query(connection: Union[cx_Oracle.Connection, oracledb.Connection], query: str, params: Dict[str, Any] | None = None) -> List | None:
    if not connection:
        raise Exception('Connection is none')

    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params or {})
            cursor.rowfactory = lambda *args: dict(
                zip([str.lower(d[0]) for d in cursor.description], args))
            results = cursor.fetchall()
            return results
    except (cx_Oracle.Error, oracledb.Error) as e:
        print(f"Error executing query: {e}")
        return None

def read_query_from_file(file_path: str, **kwargs: Any) -> str:
    """
    Read a SQL query from a file and render it using Jinja2.

    :param file_path: Path to the SQL file
    :param kwargs: Parameters to be passed to the Jinja2 template
    :return: Rendered SQL query as a string
    """
    file_content = Path(file_path).read_text()
    template = Template(file_content)
    return template.render(**kwargs)

def get_recebimento_benner(nr_pedido_fq: str, receita_master: str) -> List[Recebimento]:
    user, password, dsn = get_db_credentials(
        'BENNER_USER', 'BENNER_PASSWORD', 'BENNER_DSN')

    if (not user or not password or not dsn):
        raise Exception('user, password and dsn to be informed')

    # Using cx_Oracle for this connection
    with create_cx_oracle_connection(user, password, dsn) as connection:
        query = read_query_from_file(
            'benner.sql', nr_pedido_fq=nr_pedido_fq, receita_master=receita_master)
        results = execute_query(connection, query)
        if not results:
            return None
        return [Recebimento(**r) for r in results]
    return None    

def get_oportunidades_dcaf(data_inicial: str, data_final: str) -> List[Oportunidade] | None:
    """
    Retrieve oportunidades from DCAF using the provided date range.

    :param data_inicial: Start date for the query
    :param data_final: End date for the query
    :return: List of oportunidades
    """
    user, password, dsn = get_db_credentials(
        'DCAF_USER', 'DCAF_PASSWORD', 'DCAF_DSN')

    if (not user or not password or not dsn):
        raise Exception('user, password and dsn to be informed')

    # Using oracledb for this connection
    with create_oracledb_connection(user, password, dsn) as connection:
        query = read_query_from_file(
            'dcaf.sql', data_inicial=data_inicial, data_final=data_final)
        results = execute_query(connection, query)
        if not results:
            return None
        return [Oportunidade(**r) for r in results]
    return None


def get_dados_provisionamento()-> List[Provisionamento] | None:
    # query do painel
    user, password, dsn = get_db_credentials(
        'BENNER_USER', 'BENNER_PASSWORD', 'BENNER_DSN')
    
    if (not user or not password or not dsn):
        raise Exception('user, password and dsn to be informed')

    with create_cx_oracle_connection(user, password, dsn) as connection:
        query = read_query_from_file("provisionamento.sql")
        results = execute_query(connection, query)
        if not results:
            return None
        return [Provisionamento(**r) for r in results]
    return None

def get_dados_recebimento()-> List[RecebimentoDetalhado] | None:
    # query do painel
    user, password, dsn = get_db_credentials(
        'BENNER_USER', 'BENNER_PASSWORD', 'BENNER_DSN')
    
    if (not user or not password or not dsn):
        raise Exception('user, password and dsn to be informed')

    with create_cx_oracle_connection(user, password, dsn) as connection:
        query = read_query_from_file("recebimento_detalhado.sql")
        results = execute_query(connection, query)
        if not results:
            return None
        return [RecebimentoDetalhado(**r) for r in results]
    return None

# Example usage:
# user, password, dsn = get_db_credentials('SOME_USER', 'SOME_PASSWORD', 'SOME_DSN')
# with create_cx_oracle_connection(user, password, dsn) as connection1:
#     # Use connection1 for cx_Oracle operations
#
# with create_oracledb_connection(user, password, dsn) as connection2:
#     # Use connection2 for oracledb operations
