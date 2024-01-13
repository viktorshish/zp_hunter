import json

import requests


def get_vacancy(period=None):
    payload = {'professional_role': '96', 'area': '1', 'per_page': '100'}
    if period is not None:
        payload['period'] = period
    response = requests.get('https://api.hh.ru/vacancies', params=payload)
    response.raise_for_status()
    return response.json()


def save_in_txt_file(vacancies):
    with open('vacansys.txt', 'w', encoding='utf-8') as file:
        file.write(json.dumps(vacancies, ensure_ascii=False, indent=4))


def comparing_by_period():
    periods = [30, None]
    for period in periods:
        if period:
            print(f'Число вакансий за последний месяц в Москве: {get_vacancy(period)["found"]}')
        else:
            print(f'Число вакансий за все время в Москве: {get_vacancy()["found"]}')


def compare_languages(vacancies):
    languages = ['Python', 'C#', 'C', 'C++', 'Java', 'Javascript', 'PHP', 'Ruby', 'Go', 'TypeScript']
    languages_count = {}
    for language in languages:
        count = 0
        for vacancy in vacancies['items']:
            if language in (vacancy['name'] or vacancy['snippet']['requirement'] or vacancy['snippet']['responsibility']):
                count += 1
        languages_count[language] = count
    print(languages_count)


def get_salaries_by_vacancies(vacancies):
    for vacancy in vacancies['items']:
        print(vacancy)
        if 'Python' in (vacancy['name'] or vacancy['snippet']['requirement'] or vacancy['snippet']['responsibility']):
            print(vacancy['salary'])


def main():
    comparing_by_period()

    vacancies = get_vacancy()
    save_in_txt_file(vacancies)

    compare_languages(vacancies)

    get_salaries_by_vacancies(vacancies)


if __name__ == '__main__':
    main()
