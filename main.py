import requests


payload = {'professional_role': '96', 'area': '1', 'period': 30}
response = requests.get('https://api.hh.ru/vacancies', params=payload)
monthly_moscow_vacancies_found = response.json()['found']
print('Найдено вакансий за месяц в Москве: ', monthly_moscow_vacancies_found)

payload = {'professional_role': '96', 'area': '1'}
response = requests.get('https://api.hh.ru/vacancies', params=payload)
moscow_vacancies_found = response.json()['found']
print('Найдено вакансий за все время в Москве: ', monthly_moscow_vacancies_found)