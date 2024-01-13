import json

import requests


def get_vacancy(period=None):
    payload = {'professional_role': '96', 'area': '1', 'per_page': '100'}
    if period is not None:
        payload['period'] = period
    response = requests.get('https://api.hh.ru/vacancies', params=payload)
    response.raise_for_status()
    return response.json()


def save_in_txt_file():
    vacancies = get_vacancy()
    with open('vacansys.txt', 'w', encoding='utf-8') as file:
        file.write(json.dumps(vacancies, ensure_ascii=False, indent=4))


def compare_languages():
    languages = ['Python', 'C#', 'C', 'C++', 'Java', 'Javascript', 'PHP', 'Ruby', 'Go', 'TypeScript']
    languages_count = {}
    for language in languages:
        count = 0
        for vacancy in get_vacancy()['items']:
            if language in vacancy['name']:
                count+=1
        languages_count[language] = count
    print(languages_count)


def main():
    periods = [30, None]
    for period in periods:
        if period:
            print(f'Число вакансий за последний месяц в Москве: {get_vacancy(period)["found"]}')
        else:
            print(f'Число вакансий за все время в Москве: {get_vacancy()["found"]}')
    save_in_txt_file()
    compare_languages()


if __name__ == '__main__':
    main()
