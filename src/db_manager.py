import psycopg2

from src.config import config


class DBManager:
    def __init__(self, db_name):
        self.__db_name = db_name

    def execute_query(self, query, parameters=None):
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

    def get_all_employers(self):
        """Получает список всех компаний"""
        return self.execute_query('SELECT * FROM employers')

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой"""
        return self.execute_query('SELECT employer, COUNT(*) FROM vacancies GROUP BY employer')

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию"""
        return self.execute_query('SELECT employer, name, salary_from, salary_to, url FROM vacancies')

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям"""
        return self.execute_query('SELECT AVG(salary_from), AVG(salary_to) FROM vacancies')

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        return self.execute_query(
            'SELECT * FROM vacancies WHERE salary_from > (SELECT AVG(salary_from) FROM vacancies) '
            'OR salary_to > (SELECT AVG(salary_to) FROM vacancies)')

    def get_vacancies_with_keyword(self, keyword):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python"""
        return self.execute_query(f'SELECT * FROM vacancies WHERE name LIKE %s', (f'%{keyword}%',))
