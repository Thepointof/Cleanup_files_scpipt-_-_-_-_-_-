"""Модуль работает с терминалом и путями к папкам, проверяя наличие указанной папки + создает папку архив"""

import sys
from pathlib import Path

def get_args():
    # Условный оператор, который проверяет что бы аргументов передоваемых терминалом было 3.
    if len(sys.argv) < 3:
        print('Как использовать: Проходим в директорию папки которую нужно проверить ->'
            'вводим - python monitor.py <путь к папке> <колличество дней файла, после которых он за архивируется>')
        sys.exit(1)
    folder_path = sys.argv[1] # второй аргумент, положение папки
    days_limit = int(sys.argv[2]) # третий аргумент, время, переводим в число
    return(folder_path, days_limit)

def is_folder_exist(folder_path: str):
    # Проверяем существует ли указанная папка, по указанному пути
    folder = Path(folder_path)
    if not folder.exists():
        print(f'Папака {folder_path} не существует')
        sys.exit(1)
    if not folder.is_dir():
        print(f'{folder_path} - Это не папка')
        sys.exit(1)
    return(folder)

def prepare_archive(folder):
    archive_folder = folder / "архив"
    archive_folder.mkdir(exist_ok=True) # Создаем папку архив, если её нет
    return(archive_folder)

def log_in_folder(folder: Path):
    log_file = folder / "monitor.log"
    return(log_file)