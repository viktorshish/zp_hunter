from pprint import pprint
import json

import requests


LANGUAGES = ['Python', 'C#', 'C++', 'Java', 'Javascript', 'PHP', 'Ruby', 'Go']


def get_all_vacancies(language):
    page = 0
    pages_number = 1
    vacancies = []
    while page < pages_number:
        payload = {'professional_role': '96', 'area': '1', 'text': language, 'page': page}
        response = requests.get('https://api.hh.ru/vacancies', params=payload)
        response.raise_for_status()
        response_json = json.loads(response.text)
        vacancies.extend(response_json['items'])
        pages_number = response_json['pages']
        page += 1
    return vacancies


def predict_rub_salary(salary):
    if salary and ('RUR' in salary['currency']):
        if salary.get('from') and salary.get('to'):
            return (int(salary['from']) + int(salary['to'])) / 2
        elif salary.get('from'):
            return int(salary['from']) * 1.2
        elif salary.get('to'):
            return int(salary['to']) * 0.8


def main():
    comparison_of_languages_by_vacancies = {}
    for language in LANGUAGES:
        vacancies = get_all_vacancies(language)
        count_vacancies_with_salary = 0
        amount_salary = 0
        for vacancy in vacancies['items']:
            predicted_salary = predict_rub_salary(vacancy['salary'])
            if predicted_salary is not None:
                amount_salary += predict_rub_salary(vacancy['salary'])
                count_vacancies_with_salary += 1
        average = int(amount_salary / count_vacancies_with_salary)

        comparison_of_languages_by_vacancies[language] = {
            'vacansies_found': vacancies['found'],
            'vacancies_processed': count_vacancies_with_salary,
            'average_salary': average
        }

    pprint(comparison_of_languages_by_vacancies)


if __name__ == '__main__':
    main()
