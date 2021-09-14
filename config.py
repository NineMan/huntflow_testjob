from argparse import ArgumentParser
from pathlib import Path


class Config:
    BASE_DIR = Path(__file__).parent.absolute()
    EXCEL_FILENAME = 'Тестовая база.xlsx'
    EXCEL_SHEET = 'Лист1'
    API_URL = 'https://dev-100-api.huntflow.dev/'

    def __init__(self):
        args = parse_command_line()
        self.token = args.token
        self.file_path = self.BASE_DIR / args.path


def parse_command_line():
    parser = ArgumentParser(description='some description')
    parser.add_argument('-p', '--path', type=str, help='Relative path for input excel db', required=True)
    parser.add_argument('-t', '--token', type=str, help='HuntFlow API token', required=True)
    args = parser.parse_args()
    return args
