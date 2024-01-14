import requests


def get_vacancies():
    payload = {'professional_role': '96', 'area': '1', 'per_page': '100'}
    response = requests.get('https://api.hh.ru/vacancies', params=payload)
    response.raise_for_status()
    return response.json()


def compare_languages(vacancies):
    languages = ['Python', 'C#', 'C++', 'Java', 'Javascript', 'PHP', 'Ruby', 'Go', 'TypeScript']
    languages_count = {}
    for language in languages:
        count = 0
        for vacancy in vacancies['items']:
            if language in vacancy['name']:
                count += 1
            elif (vacancy['snippet'].get('requirement') is not None
                  and language in vacancy['snippet']['requirement']):
                count += 1
            elif (vacancy['snippet'].get('responsibility') is not None
                  and language in vacancy['snippet']['responsibility']):
                count += 1
        languages_count[language] = count
    print(languages_count)


def find_salary_by_language(vacancies, language):
    for vacancy in vacancies['items']:
        if language.lower() in vacancy['name'].lower():
            print(f">>>>> {vacancy['salary']} : {vacancy['name']}")
            print(predict_rub_salary(vacancy['salary']))

        elif (vacancy['snippet'].get('requirement') is not None
              and language.lower() in vacancy['snippet']['requirement'].lower()):
            print(f">>>>> {vacancy['salary']} : {vacancy['name']} -  {vacancy['snippet']['requirement']}")
            print(predict_rub_salary(vacancy['salary']))

        elif (vacancy['snippet'].get('responsibility') is not None
              and language.lower() in vacancy['snippet']['responsibility'].lower()):
            print(f">>>>> {vacancy['salary']} : {vacancy['name']} - {vacancy['snippet']['responsibility']}")
            print(predict_rub_salary(vacancy['salary']))


def predict_rub_salary(salary):
    if salary and 'RUR' in salary['currency']:
        if salary.get('from') and salary.get('to'):
            return (int(salary['from']) + int(salary['to'])) / 2
        elif salary.get('from'):
            return int(salary['from']) * 1.2
        elif salary.get('to'):
            return int(salary['to']) * 0.8


def main():
    vacancies = get_vacancies()
    compare_languages(vacancies)

    print(find_salary_by_language(vacancies, 'python'))
    # predict_rub_salary_by_language(vacancies)


if __name__ == '__main__':
    main()
