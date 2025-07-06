import requests


class HHParser:
    def __init__(self):
        self.__url_employer = 'https://api.hh.ru/employers'
        self.__url_vacancies = 'https://api.hh.ru/vacancies'

    def get_employers(self):
        params = {'sort_by': 'by_vacancies_open', 'per_page': 10}
        response = requests.get(self.__url_employer, params=params)
        response.raise_for_status()
        employers = response.json()['items']
        return [{'id': employer['id'], 'name': employer['name']} for employer in employers]

    def get_vacancies_by_employers(self, employer_id):
        params = {'employer_id': employer_id, 'per_page': 50}
        response = requests.get(self.__url_vacancies, params=params)
        response.raise_for_status()
        vacancies = response.json()['items']

        return vacancies

        # return [{'id': vacancy['id'], 'name': vacancy['name']} for vacancy in vacancies]
        # return [{'id': vacancy['id'],
        #          'name': vacancy['name'],
        #          'area': vacancy['area']['name'],
        #          'employer': vacancy['employer']['name'],
        #          'url': vacancy['alternate_url']}
        #         for vacancy in vacancies]

    def get_all_vacancies_by_employers(self):
        employers = self.get_employers()
        all_vacancies = []
        for employer in employers:
            vacancies = self.get_vacancies_by_employers(employer['id'])
            all_vacancies.extend([self.filter_vacancy(vacancy) for vacancy in vacancies])
        return all_vacancies

    @staticmethod
    def filter_vacancy(vacancy):
        salary = vacancy.get('salary', {})
        salary_from = salary.get('from', 0) if salary else 0
        salary_to = salary.get('to', 0) if salary else 0

        return {'id': vacancy['id'],
                'name': vacancy['name'],
                'area': vacancy['area']['name'],
                'salary_from': salary_from,
                'salary_to': salary_to,
                'employer': vacancy['employer']['name'],
                'employer_id': vacancy['employer']['id'],
                'url': vacancy['alternate_url']}


# hh = HHParser()
# # print(hh.get_vacancies_by_employers(3529))
# print(hh.get_all_vacancies_by_employers())
# # print(hh.get_employers())
