import time

from environs import Env
import requests
from terminaltables import AsciiTable


LANGUAGES = ['Python', 'C#', 'C++', 'Java', 'Javascript', 'PHP', 'Ruby', 'Go']
HH_PROGRAMMER_DEVELOPER_ID = '96'
HH_MOSCOW_ID = '1'
SJ_PROGRAMMER_DEVELOPER_ID = 33
SJ_MOSCOW_ID = 4


def get_hh_vacancies_response(page, language):
    page_vacancies = 100
    params = {
        'professional_role': HH_PROGRAMMER_DEVELOPER_ID,
        'area': HH_MOSCOW_ID,
        'text': language,
        'page': page,
        'per_page': page_vacancies,
        'currency': 'RUR'
    }
    url = 'https://api.hh.ru/vacancies'

    page_response = requests.get(url, params=params)
    page_response.raise_for_status()
    return page_response.json()


def get_vacancies_hh(language):
    vacancies = []
    page = 0
    while True:
        page_response = get_hh_vacancies_response(page, language)
        page_vacancies = page_response['items']
        vacancies.extend(page_vacancies)

        if page+1 >= page_response['pages']:
            break
        page += 1
        time.sleep(5)
    found_vacancies = page_response['found']
    return vacancies, found_vacancies


def predict_rub_salary(vacancy):
    if vacancy.get('salary'):
        from_salary = vacancy['salary'].get('from')
        to_salary = vacancy['salary'].get('to')
    elif vacancy.get('currency'):
        from_salary = vacancy.get('payment_from')
        to_salary = vacancy['payment_to']
    else:
        return None

    if from_salary and to_salary:
        return (int(from_salary) + int(to_salary)) / 2
    elif from_salary:
        return int(from_salary) * 1.2
    elif to_salary:
        return int(to_salary) * 0.8
    else:
        return None


def calculate_the_average_salary(vacancies, found_vacancies):
    count_vacancies_with_salary = 0
    amount_salary = 0
    for vacancy in vacancies:
        predicted_salary = predict_rub_salary(vacancy)

        if predicted_salary:
            amount_salary += predicted_salary
            count_vacancies_with_salary += 1

    try:
        average = int(amount_salary / count_vacancies_with_salary)
    except ZeroDivisionError:
        average = 0
    return {
        'vacancies_found': found_vacancies,
        'vacancies_processed': count_vacancies_with_salary,
        'average_salary': average
    }


def get_sj_vacancies_response(page, language, sj_key):
    headers = {'X-Api-App-Id': sj_key}
    params = {
        'town': SJ_MOSCOW_ID,
        'catalogues': SJ_PROGRAMMER_DEVELOPER_ID,
        'keyword': language,
        'page': page
    }
    url = 'https://api.superjob.ru/2.2/vacancies/'

    page_response = requests.get(url, headers=headers, params=params)
    page_response.raise_for_status()
    return page_response.json()


def get_vacancies_sj(language, sj_key):
    vacancies = []
    page = 0
    while True:
        page_response = get_sj_vacancies_response(page, language, sj_key)
        page_vacancies = page_response['objects']
        vacancies.extend(page_vacancies)

        if not page_response['more']:
            break
        page += 1
    found_vacancies = page_response['total']
    return vacancies, found_vacancies


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

    hh_comparison_vacancies = {}
    sj_comparison_vacancies = {}
    for language in LANGUAGES:
        hh_vacancies, hh_found_vacancies = get_vacancies_hh(language)
        hh_average_salaries = calculate_the_average_salary(
            hh_vacancies,
            hh_found_vacancies
        )
        hh_comparison_vacancies[language] = hh_average_salaries

        sj_vacancies, sj_found_vacancies = get_vacancies_sj(language, sj_key)
        sj_average_salaries = calculate_the_average_salary(
            sj_vacancies,
            sj_found_vacancies
        )
        sj_comparison_vacancies[language] = sj_average_salaries

    print(convert_statistics_to_table(hh_comparison_vacancies, 'HeadHunter Moscow'))
    print(convert_statistics_to_table(sj_comparison_vacancies, 'SuperJob Moscow'))


if __name__ == '__main__':
    main()
