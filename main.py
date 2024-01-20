import requests


LANGUAGES = ['Python', 'C#', 'C++', 'Java', 'Javascript', 'PHP', 'Ruby', 'Go']


def get_all_vacancies(language):
    vacancies = []
    page = 0

    while True:
        params = {
            'professional_role': '96',
            'area': '1',
            'text': language,
            'page': page
        }
        url = 'https://api.hh.ru/vacancies'
        page_response = requests.get(url, params=params)
        page_response.raise_for_status()
        page_vacancies = page_response.json()['items']
        vacancies.extend(page_vacancies)

        if page+1 >= page_response.json()['pages']:
            break
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


def calculate_the_average_salary_by_language_hh():
    comparison_of_languages_by_vacancies = {}

    for language in LANGUAGES:
        vacancies = get_all_vacancies(language)

        count_vacancies_with_salary = 0
        amount_salary = 0

        for vacancy in vacancies:
            predicted_salary = predict_rub_salary(vacancy['salary'])

            if predicted_salary is not None:
                amount_salary += predict_rub_salary(vacancy['salary'])
                count_vacancies_with_salary += 1
        average = int(amount_salary / count_vacancies_with_salary)

        comparison_of_languages_by_vacancies[language] = {
            'vacancies_found': len(vacancies),
            'vacancies_processed': count_vacancies_with_salary,
            'average_salary': average
        }
    return comparison_of_languages_by_vacancies


def main():
    print(calculate_the_average_salary_by_language_hh())

if __name__ == '__main__':
    main()
