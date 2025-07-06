from src.utils import create_database, create_tables, insert_datatables
from src.db_manager import DBManager

name_db = "test_job_search_db"
create_database(name_db)
create_tables(name_db)
insert_datatables(name_db)

db_manager = DBManager(name_db)

while True:
    print("Доступные операции с базой данных по вакансиям:")
    print("""
        1 - Получить список всех компаний и количество вакансий у каждой;
        2 - Получить список всех вакансий с указанием названия компании,
            названия вакансии и зарплаты и ссылки на вакансию;
        3 - Получить среднюю зарплату по вакансиям;
        4 - Получить список всех вакансий, у которых зарплата выше средней по всем вакансиям;
        5 - Получить список всех вакансий, в названии которых содержатся переданные в метод слова;
        6 - Выход из программы
        """)
    answer = input("Введите число:    ")
    if answer == "1":
        for elem in db_manager.get_companies_and_vacancies_count():
            print(f"Название компании: {elem[0]}", f"Количество вакансий: {elem[1]}", sep="\n")
            print()
    elif answer == "2":
        for elem in db_manager.get_all_vacancies():
            print(f"Название компании: {elem[0]}", f"Название вакансии: {elem[1]}", f"Зарплата от: {elem[2]}", f"Зарплата до: {elem[3]}", f"Ссылка на вакансию: {elem[4]}", sep='\n')
            print()
    elif answer == "3":
        for elem in db_manager.get_avg_salary():
            print(f"Средняя зарплата от: {int(elem[0])}", f"Средняя зарплата до: {int(elem[1])}", sep="\n")
            print()
    elif answer == "4":
        for elem in db_manager.get_vacancies_with_higher_salary():
            print(f"Название вакансии: {elem[2]}", f"Город: {elem[3]}", f"Зарплата от: {elem[4]}",
                  f"Зарплата до: {elem[5]}", f"Название компании: {elem[6]}", f"Ссылка на вакансию: {elem[7]}",
                  sep='\n')
            print()
    elif answer == "5":
        keyword = input("Введите интересующее слово в названии вакансии:    ")
        result = db_manager.get_vacancies_with_keyword(keyword)
        if result:
            for elem in result:
                print(f"Название вакансии: {elem[2]}", f"Город: {elem[3]}", f"Зарплата от: {elem[4]}",
                      f"Зарплата до: {elem[5]}", f"Название компании: {elem[6]}", f"Ссылка на вакансию: {elem[7]}",
                      sep='\n')
                print()
        else:
            print("Вакансии с введенным словом не найдены")
    elif answer == "6":
        break
    else:
        print("Введите число из указанного списка")
