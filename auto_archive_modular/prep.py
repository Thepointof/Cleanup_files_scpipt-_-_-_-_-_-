"""Модуль работает с терминалом и путями к папкам, проверяя наличие указанной папки + создает папку архив"""
import os
import msvcrt
import sys
import datetime
from pathlib import Path

def get_args():
    # Условный оператор, который проверяет что бы аргументов передоваемых терминалом было 3.
    if len(sys.argv) < 3:
        print('Как использовать: Проходим в директорию папки которую нужно проверить ->'
            'вводим - python monitor.py <путь к папке> <колличество дней файла, после которых он за архивируется>')
        sys.exit(1)
    folder_path = sys.argv[1] # второй аргумент, положение папки
    days_limit = int(sys.argv[2]) # третий аргумент, время, переводим в число
    return folder_path, days_limit 

def is_folder_exist(folder_path: str):
    # Проверяем существует ли указанная папка, по указанному пути
    folder = Path(folder_path)
    if not folder.exists():
        print(f'Папака {folder_path} не существует')
        sys.exit(1)
    if not folder.is_dir():
        print(f'{folder_path} - Это не папка')
        sys.exit(1)
    return folder 

def prepare_archive(folder):
    now = datetime.datetime.now() # Берем текущую дату
    arc_name = (f'archive_{now:%Y-%m-%d_%H-%M-%S}.zip') # Создаем название архива использую текущую дату
    archive_file = folder / arc_name # Соединяем архив с папкой
    return archive_file # Возвращаем путь с именем

def log_in_folder(folder: Path):
    log_file = folder / "monitor.log"
    return log_file 

def is_locked(file_path): # Проверяем при помощи msvcrt занятость файла перед переносом в архив. Только для Windows.
    try:
        fd = os.open(file_path, os.O_RDWR) # Открваем файловый дескриптор, проверяем занятость файла
    except PermissionError:
        return True # Если не смог открыться занят или нет прав

    try:
        msvcrt.locking(fd, msvcrt.LK_NBLCK , 1) # Пытаемся блокировать 1 байт файла
        msvcrt.locking(fd, msvcrt.LK_UNLCK, 1) # Разблокируем байт
        return False # Если файл блокирует и разблокируется, он не занят другими процессами
    except OSError:
        return True # Если файл занят возвращяет True
    finally:
        os.close(fd) #  Закрываем файлоый дескриптор