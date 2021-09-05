from config import Config
from excel import start_service


class NoTokenError(Exception):
    pass


class ExcelPathNotFoundError(Exception):
    pass


def main():
    # Читаем командную строку, записываем в конфиг
    cfg = Config()

    # Проверяем наличие токена
    if not cfg.token:
        raise NoTokenError(f'Need to specify the token')

    # Проверяем наличие директории db
    if not cfg.file_path.is_dir():
        raise ExcelPathNotFoundError(f'No such directory')

    # Запускаем основной скрипт
    start_service(cfg)


if __name__ == '__main__':
    main()
