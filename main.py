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
    return vacancies


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


def calculate_the_average_salary_for_language(vacancies, found_vacancies):
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
        'town': ID_SJ_MOSCOW,
        'catalogues': ID_SJ_PROGRAMMER_DEVELOPER,
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
    return vacancies


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

    comparison_vacancies_hh = {}
    comparison_vacancies_sj = {}
    for language in LANGUAGES:
        hh_found_vacancies = get_hh_vacancies_response(0, language)['found']
        vacancies_hh = get_vacancies_hh(language)
        average_salaries_hh = calculate_the_average_salary_for_language(vacancies_hh, hh_found_vacancies)
        comparison_of_languages_by_vacancies_hh[language] = average_salaries_hh

        sj_found_vacancies = get_sj_vacancies_response(0, language, sj_key)['total']
        vacancies_sj = get_vacancies_sj(language, sj_key)
        average_salaries_sj = calculate_the_average_salary_for_language(vacancies_sj, sj_found_vacancies)
        comparison_of_languages_by_vacancies_sj[language] = average_salaries_sj

    print(convert_statistics_to_table(comparison_of_languages_by_vacancies_hh, 'HeadHunter Moscow'))
    print(convert_statistics_to_table(comparison_of_languages_by_vacancies_sj, 'SuperJob Moscow'))


if __name__ == '__main__':
    main()
