import requests


def get_vacancies(language):
    payload = {'professional_role': '96', 'area': '1', 'per_page': '20', 'text': language}
    response = requests.get('https://api.hh.ru/vacancies', params=payload)
    response.raise_for_status()
    return response.json()


def find_salary_by_language(vacancies, language):
    for vacancy in vacancies['items']:
        if language.lower() in vacancy['name'].lower():
            print(predict_rub_salary(vacancy['salary']))

        elif (vacancy['snippet'].get('requirement') is not None and
              language.lower() in vacancy['snippet']['requirement'].lower()):
            print(predict_rub_salary(vacancy['salary']))

        elif (vacancy['snippet'].get('responsibility') is not None and
              language.lower() in vacancy['snippet']['responsibility'].lower()):
            print(predict_rub_salary(vacancy['salary']))


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


def main():
    languages = ['Python', 'C#', 'C++', 'Java', 'Javascript',
                 'PHP', 'Ruby', 'Go', 'TypeScript']
    languages_count = {}
    for language in languages:
        languages_count[language] = get_vacancies(language)['found']
    print(languages_count)


if __name__ == '__main__':
    main()
