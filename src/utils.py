import psycopg2
from src.config import config
from src.hh_api import HHParser


def create_database(name_db: str) -> None:
    """
        Создает новую базу данных
        Args:
            name_db: название базы данных
        """
    params = config()
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    # Закрываем все активные подключения к базе данных
    cur.execute(f"""
            SELECT pg_terminate_backend(pg_stat_activity.pid)
            FROM pg_stat_activity
            WHERE pg_stat_activity.datname = '{name_db}'
            AND pid <> pg_backend_pid()
        """)

    cur.execute(f'DROP DATABASE IF EXISTS {name_db}')
    cur.execute(f'CREATE DATABASE {name_db}')

    cur.close()
    conn.close()


def create_tables(name_db: str) -> None:
    """
        Создает таблицы в базе данных
        Args:
            name_db: название базы данных
        """
    params = config()
    conn = psycopg2.connect(dbname=name_db, **params)
    with conn:
        with conn.cursor() as cur:
            # Т.к. в таблице vacancies присутствует внешний ключ на таблицу employers,
            # то таблица employers должна создаваться первой
            cur.execute("""CREATE TABLE employers(
                        id int PRIMARY KEY,
                        name varchar(255) NOT NULL
                        )""")
            # использую внешний ключ на таблицу кампаний
            cur.execute("""CREATE TABLE vacancies(
                        id int PRIMARY KEY,
                        employer_id int REFERENCES employers(id),
                        name varchar(255) NOT NULL,
                        area varchar(255),
                        salary_from int,
                        salary_to int,
                        employer varchar(255),
                        url varchar(255)
                        )""")
    conn.close()


def insert_datatables(name_db: str) -> None:
    """
        Заполняет таблицы данными
        Args:
            name_db: название базы данных
        """
    hh_parser = HHParser()
    employers = hh_parser.get_employers()
    vacancies = hh_parser.get_all_vacancies_by_employers()
    params = config()
    conn = psycopg2.connect(dbname=name_db, **params)
    with conn:
        with conn.cursor() as cur:
            for employer in employers:
                cur.execute('INSERT INTO employers VALUES (%s, %s)', (employer['id'], employer['name']))
            for vacancy in vacancies:
                cur.execute('INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
                            (vacancy['id'], vacancy['employer_id'], vacancy['name'], vacancy['area'],
                             vacancy['salary_from'], vacancy['salary_to'], vacancy['employer'], vacancy['url']))
    conn.close()
