from pprint import pprint

import requests


LANGUAGES = ['Python', 'C#', 'C++', 'Java', 'Javascript', 'PHP', 'Ruby', 'Go']


def get_vacancies(language):
    payload = {'professional_role': '96', 'area': '1', 'text': language}
    response = requests.get('https://api.hh.ru/vacancies', params=payload)
    response.raise_for_status()
    return response.json()


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
        vacancies = get_vacancies(language)
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
