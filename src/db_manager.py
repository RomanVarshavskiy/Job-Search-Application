from typing import Optional
import psycopg2

from src.config import config


class DBManager:
    """Класс для работы с базой данных вакансий и работодателей"""
    def __init__(self, db_name: str) -> None:
        """Инициализация менеджера базы данных"""
        self.__db_name = db_name

    def execute_query(self, query: str, parameters: Optional[tuple] = None) -> list[tuple]:
        """Выполняет SQL-запрос к базе данных.
           Args:
               query: SQL-запрос
               parameters: параметры запроса (опционально)"""
        params = config()
        conn = psycopg2.connect(dbname=self.__db_name, **params)
        with conn:
            with conn.cursor() as cur:
                if parameters is not None:
                    cur.execute(query, parameters)
                else:
                    cur.execute(query)
                res = cur.fetchall()
        cur.close()
        conn.close()
        return res


    def get_companies_and_vacancies_count(self) -> list[tuple]:
        """Получает список всех компаний и количество вакансий у каждой"""
        return self.execute_query('SELECT employer, COUNT(*) FROM vacancies GROUP BY employer')

    def get_all_vacancies(self) -> list[tuple]:
        """Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию"""
        return self.execute_query('SELECT employer, name, salary_from, salary_to, url FROM vacancies')

    def get_avg_salary(self) -> list[tuple]:
        """Получает среднюю зарплату по вакансиям"""
        return self.execute_query('SELECT AVG(salary_from), AVG(salary_to) FROM vacancies')

    def get_vacancies_with_higher_salary(self)-> list[tuple]:
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        return self.execute_query(
            'SELECT * FROM vacancies WHERE salary_from > (SELECT AVG(salary_from) FROM vacancies) '
            'OR salary_to > (SELECT AVG(salary_to) FROM vacancies)')

    def get_vacancies_with_keyword(self, keyword: str) -> list[tuple]:
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова
            Args:
                keyword: ключевое слово для поиска в названии вакансии"""
        return self.execute_query(f'SELECT * FROM vacancies WHERE name LIKE %s', (f'%{keyword}%',))
