import time

import requests
from terminaltables import AsciiTable

import settings


def get_all_vacancies(language):
    vacancies = []
    page = 0

    while True:
        params = {
            'professional_role': '96',
            'area': '1',
            'text': language,
            'page': page
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


def calculate_the_average_salary_by_language_hh():
    comparison_of_languages_by_vacancies = {}

    for language in settings.LANGUAGES:
        vacancies = get_all_vacancies(language)

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

        comparison_of_languages_by_vacancies[language] = {
            'vacancies_found': len(vacancies),
            'vacancies_processed': count_vacancies_with_salary,
            'average_salary': average
        }
    return comparison_of_languages_by_vacancies


def get_all_vacancies_from_sj(language):
    vacancies = []
    page = 0

    while True:
        headers = {'X-Api-App-Id': settings.SB_KEY}
        params = {
            'town': 4,
            'catalogues': 33,
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


def calculate_the_average_salary_by_language_sj():
    comparison_of_languages_by_vacancies = {}

    for language in settings.LANGUAGES:
        vacancies = get_all_vacancies_from_sj(language)

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

        comparison_of_languages_by_vacancies[language] = {
            'vacancies_found': len(vacancies),
            'vacancies_processed': count_vacancies_with_salary,
            'average_salary': average
        }
    return comparison_of_languages_by_vacancies


def convert_statistics_to_table(statistics, title):
    table_data = [
        ['Язык программирования', 'Вакансий найдено',
         'Вакансий обработано', 'Средняя зарплата'],
    ]

    for key, value in statistics.items():
        row = [key, value['vacancies_found'], value['vacancies_processed'], value['average_salary']]
        table_data.append(row)

    table = AsciiTable(table_data, title)
    print(table.table)


def main():
    convert_statistics_to_table(calculate_the_average_salary_by_language_hh(), 'HeadHunter Moscow')
    print()
    convert_statistics_to_table(calculate_the_average_salary_by_language_sj(), 'SuperJob Moscow')


if __name__ == '__main__':
    main()
