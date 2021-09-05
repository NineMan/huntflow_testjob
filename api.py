import mimetypes

import requests


class NoAccountIdFoundError(Exception):
    pass


class HuntflowAPI:

    def __init__(self, config):
        self.cfg = config
        self.url = self.cfg.API_URL
        self.headers = {
            'User-Agent': 'App/1.0 (test@huntflow.ru)',
            'Accept': '*/*',
            'Authorization': 'Bearer ' + self.cfg.token,
        }
        self.account_id = self.set_account_id()
        self.list_statuses = self.get_list_statuses()
        self.list_vacancies = self.get_list_vacancies()

    def get_me(self):
        url = self.url + 'me'
        response = requests.get(url, headers=self.headers).json()
        response.raise_for_status()
        return response.json()

    def get_accounts(self):
        """Возвращает список этапов подбора"""

        url = self.url + 'accounts'
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def set_account_id(self):
        try:
            accounts = self.get_accounts().get('items')
            return accounts[0].get('id')
        except Exception:
            raise NoAccountIdFoundError

    def get_sources(self):
        """Возвращает список источников резюме"""

        url = self.url + f'account/{self.account_id}/applicant/sources'
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_applicants(self):
        """Возвращает список кандидатов"""

        url = self.url + f'account/{self.account_id}/applicants'
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_vacancies(self):
        """Возвращает список вакансий"""

        url = self.url + f'account/{self.account_id}/vacancies'
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_statuses(self):
        """Возвращает список этапов подбора (статусов)."""

        url = self.url + f'account/{self.account_id}/vacancy/statuses'
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def post_file(self, path_filename):
        url = self.url + f'account/{self.account_id}/upload'
        headers = self.headers.copy()
        headers['X-File-Parse'] = 'true'
        filename = path_filename.split('/')[-1]
        files = {'file': (filename, open(path_filename, 'rb'), self.get_mimetype(filename))}

        return requests.post(url, headers=headers, files=files)

    def post_applicant(self, data):
        url = self.url + f'account/{self.account_id}/applicants'
        headers = self.headers.copy()
        headers['Content-Type'] = 'application/json'
        return requests.post(url, headers=headers, json=data)

    def post_applicant_vacancy(self, applicant, vacancy_id, status_id):
        url = self.url + f'account/{self.account_id}/applicants/{applicant.id}/vacancy'

        headers = self.headers.copy()
        headers['Content-Type'] = 'application/json'
        data = {
            "vacancy": vacancy_id,
            "status": status_id,
            "comment": applicant.comment,
            "files": applicant.files_id,
            # "rejection_reason": null,
            # "fill_quota": 234
        }
        return requests.post(url, headers=headers, json=data)

    def get_list_statuses(self):
        return {status.get('name'): status.get('id') for status in self.get_statuses().get('items')}

    def get_list_vacancies(self):
        return {vacancy.get('position'): vacancy.get('id') for vacancy in self.get_vacancies().get('items')}

    @staticmethod
    def get_mimetype(filename):
        return mimetypes.guess_type(filename)[0]


# from config import Config
# cfg = Config()
# print(f'{cfg = }')
# print(f'{cfg.token = }')
# print(f'{cfg.file_path = }')
# h = HuntflowAPI(cfg)
# Статус себя
# resp = get_me()
# id = resp.get('id')
# print(f'{id}')


# Список компаний
# resp = h.get_accounts()
# print(f'{resp = }')


# Список файлов
# Загрузить файл с резюме   !!!
# ans = post_file('4.pdf')
# pprint(ans.json())
# pprint(ans.text)
# pprint(ans.text)


# Список кандидатов
# applicants = get_applicants()
# for applicant in applicants.get('items'):
#     print(f'{applicant = }')


# Загрузить кандидата
# applicant = post_applicant()
# print(f'{applicant = }')


# # Список вакансий
# vacancies = get_vacancies()
# for vacancy in vacancies.get('items'):
#     print(f'{vacancy = }')


# # Список статусов
# statuses = get_statuses()
# for status in statuses.get('items'):
#     print(f'{status = }')


# Прицепить кандидата к вакансии
# post_applicant_vacancy()


# for file in list_filenames:
#     type = get_mimetype(file)
#     print(f'{type = }')


# response = get_sources()
# for i in response.get('items'):
#     t = i.get('type')
#     if t == 'user':
#     print(i)


