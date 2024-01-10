import requests


def get_month_vacancy(period=None):
    payload = {'professional_role': '96', 'area': '1'}
    if period is not None:
        payload['period'] = period
    response = requests.get('https://api.hh.ru/vacancies', params=payload)
    response.raise_for_status()
    print(response.json())
    return response.json()['found']


if __name__ == '__main__':
    periods = [30, None]
    for period in periods:
        if period:
            print(f'Число вакансий за последний месяц в Москве: {get_month_vacancy(period)}')
        else:
            print(f'Число вакансий за все время в Москве: {get_month_vacancy()}')
