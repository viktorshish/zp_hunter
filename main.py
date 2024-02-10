import time

from environs import Env
import requests
from terminaltables import AsciiTable


LANGUAGES = ['Python', 'C#', 'C++', 'Java', 'Javascript', 'PHP', 'Ruby', 'Go']
ID_HH_PROGRAMMER_DEVELOPER = '96'
ID_HH_MOSCOW = '1'
ID_SJ_PROGRAMMER_DEVELOPER = 33
ID_SJ_MOSCOW = 4


def get_vacancies_hh(language):
    vacancies = []
    page = 0
    while True:
        vacancies_on_the_page = 100
        params = {
            'professional_role': ID_HH_PROGRAMMER_DEVELOPER,
            'area': ID_HH_MOSCOW,
            'text': language,
            'page': page,
            'per_page': vacancies_on_the_page
        }
        url = 'https://api.hh.ru/vacancies'

        page_response = requests.get(url, params=params)
        page_response.raise_for_status()
        page_vacancies = page_response.json()['items']
        vacancies.extend(page_vacancies)

        if page+1 >= page_response.json()['pages']:
            break
        page += 1
        time.sleep(1)
    return vacancies


def predict_rub_salary_hh(salary):
    if salary and ('RUR' in salary['currency']):
        if salary.get('from') and salary.get('to'):
            return (int(salary['from']) + int(salary['to'])) / 2
        elif salary.get('from'):
            return int(salary['from']) * 1.2
        elif salary.get('to'):
            return int(salary['to']) * 0.8


def calculate_the_average_salary_for_language_hh(vacancies):
    count_vacancies_with_salary = 0
    amount_salary = 0
    for vacancy in vacancies:
        predicted_salary = predict_rub_salary_hh(vacancy['salary'])

        if predicted_salary is not None:
            amount_salary += predict_rub_salary_hh(vacancy['salary'])
            count_vacancies_with_salary += 1

    try:
        average = int(amount_salary / count_vacancies_with_salary)
    except ZeroDivisionError:
        average = 0
    return {
        'vacancies_found': len(vacancies),
        'vacancies_processed': count_vacancies_with_salary,
        'average_salary': average
    }


def get_vacancies_sj(language, sj_key):
    vacancies = []
    page = 0
    while True:
        headers = {'X-Api-App-Id': sj_key}
        params = {
            'town': ID_SJ_MOSCOW,
            'catalogues': ID_SJ_PROGRAMMER_DEVELOPER,
            'keyword': language,
            'page': page
        }
        url = 'https://api.superjob.ru/2.2/vacancies/'

        page_response = requests.get(url, headers=headers, params=params)
        page_response.raise_for_status()
        page_vacancies = page_response.json()['objects']
        vacancies.extend(page_vacancies)

        if not page_response.json()['more']:
            break
        page += 1
    return vacancies


def predict_rub_salary_sj(vacancy):
    if 'rub' in vacancy['currency']:
        if vacancy.get('payment_from') and vacancy.get('payment_to'):
            return (int(vacancy['payment_from']) + int(vacancy['payment_to'])) / 2
        elif vacancy.get('payment_from'):
            return int(vacancy['payment_from']) * 1.2
        elif vacancy.get('payment_to'):
            return int(vacancy['payment_to']) * 0.8


def calculate_the_average_salary_by_language_sj(vacancies):
    count_vacancies_with_salary = 0
    amount_salary = 0
    for vacancy in vacancies:
        predicted_salary = predict_rub_salary_sj(vacancy)

        if predicted_salary is not None:
            amount_salary += predict_rub_salary_sj(vacancy)
            count_vacancies_with_salary += 1

    try:
        average = int(amount_salary / count_vacancies_with_salary)
    except ZeroDivisionError:
        average = 0
    return {
        'vacancies_found': len(vacancies),
        'vacancies_processed': count_vacancies_with_salary,
        'average_salary': average
    }


def convert_statistics_to_table(statistics, title):
    final_statistic = [
        ['Язык программирования', 'Вакансий найдено',
         'Вакансий обработано', 'Средняя зарплата'],
    ]

    for language, language_statistics in statistics.items():
        row = [
            language,
            language_statistics['vacancies_found'],
            language_statistics['vacancies_processed'],
            language_statistics['average_salary']
        ]
        final_statistic.append(row)

    table = AsciiTable(final_statistic, title)
    return table.table


def main():
    env = Env()
    env.read_env()
    sj_key = env.str("SJ_KEY")

    comparison_of_languages_by_vacancies_hh = {}
    comparison_of_languages_by_vacancies_sj = {}
    for language in LANGUAGES:
        vacancies_hh = get_vacancies_hh(language)
        average_salaries_hh = calculate_the_average_salary_for_language_hh(vacancies_hh)
        comparison_of_languages_by_vacancies_hh[language] = average_salaries_hh

        vacancies_sj = get_vacancies_sj(language, sj_key)
        average_salaries_sj = calculate_the_average_salary_by_language_sj(vacancies_sj)
        comparison_of_languages_by_vacancies_sj[language] = average_salaries_sj

    print(convert_statistics_to_table(comparison_of_languages_by_vacancies_hh, 'HeadHunter Moscow'))
    print(convert_statistics_to_table(comparison_of_languages_by_vacancies_sj, 'SuperJob Moscow'))


if __name__ == '__main__':
    main()
