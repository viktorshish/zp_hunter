import requests


payload = {'professional_role': '96'}
response = requests.get('https://api.hh.ru/vacancies', params=payload)
monthly_vacancies = response.json()
print(monthly_vacancies)
