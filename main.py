from pprint import pprint

import requests


def get_vacancies(language):
    payload = {'professional_role': '96', 'area': '1', 'text': language}
    response = requests.get('https://api.hh.ru/vacancies', params=payload)
    response.raise_for_status()
    return response.json()


def predict_rub_salary(salary):
    if salary and 'RUR' in salary['currency']:
        if salary.get('from') and salary.get('to'):
            return (int(salary['from']) + int(salary['to'])) / 2
        elif salary.get('from'):
            return int(salary['from']) * 1.2
        elif salary.get('to'):
            return int(salary['to']) * 0.8
    elif salary and not 'RUR' in salary['currency']:
        return None

def count_vacancy_salary(vacancies):
    count = 0
    for vacancy in vacancies:
        if vacancy['salary']:
            count +=1
    return count


def main():
    languages = ['Python', 'C#', 'C++', 'Java', 'Javascript',
                 'PHP', 'Ruby', 'Go', 'TypeScript']

    languages_count = {}
    for language in languages:

        vacancies = get_vacancies(language)
        average = sum(vacancies.items.salary.values()) / count_vacancy_salary(vacancies['items']
        languages_count[language] = {
            'vacansies_found': vacancies['found'],
            'vacancies_processed': count_vacancy_salary(vacancies['items']),
            'average_salary': predict_rub_salary(get_vacancies())
        }

    pprint(languages_count)


if __name__ == '__main__':
    main()
