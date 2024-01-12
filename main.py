import requests


def get_month_vacancy(period=None):
    payload = {'professional_role': '96', 'area': '1'}
    if period is not None:
        payload['period'] = period
    response = requests.get('https://api.hh.ru/vacancies', params=payload)
    response.raise_for_status()
    print(response.text)

    # with open('vacansy.txt', 'w', encoding='utf-8') as file:
    #     file.write(response.text)

    languages = ['Python', 'C#', 'C', 'C++', 'Java', 'Javascript']
    languages_count = {}
    for language in languages:
        count = 0
        for vacancy in response.json()['items']:
            if language in vacancy['name']:
                count+=1
        languages_count[language] = count
    print(languages_count)
    return response.json()['found']


if __name__ == '__main__':
    periods = [30, None]
    for period in periods:
        if period:
            print(f'Число вакансий за последний месяц в Москве: {get_month_vacancy(period)}')
        else:
            print(f'Число вакансий за все время в Москве: {get_month_vacancy()}')
