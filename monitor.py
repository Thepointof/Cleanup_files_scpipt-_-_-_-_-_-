import sys
import datetime
import shutil
import logging
from pathlib import Path

logging.basicConfig(filename='monitor.log', level=logging.INFO, format='%(asctime)s - %(message)s') # создаем лог о проделанной работе

print('Я запустился!')
print('Аргументы которе мне передали', sys.argv)

# Условный оператор, который проверяет что бы аргументов передоваемых терминалом было 3.
if len(sys.argv) < 3:
    print('Как использовать: Проходим в директорию папки которую нужно проверить ->'
          'вводим - python monitor.py <путь к папке> <колличество дней файла, после которых он за архивируется>')
    sys.exit(1)
folder_path = sys.argv[1] # второй аргумент, положение папки
days_limit = int(sys.argv[2]) # третий аргумент, время, переводим в число

logging.info(f'Запуск мониторинга папки {folder_path}, лимит {days_limit} дней') # выводим сообщение лога 

# Проверяем существует ли указанная папка, по указанному пути
folder = Path(folder_path)
if not folder.exists():
    print(f'Папака {folder_path} не существует')
    sys.exit(1)
if not folder.is_dir():
    print(f'{folder_path} - Это не папка')
    sys.exit(1)

archive_folder = folder / "архив"
archive_folder.mkdir(exist_ok=True) # Создаем папку архив, если её нет

files_counter = {'перемещено': 0, 'оставленно': 0, 'проверенно': 0} # Словарь со счётчиком файлов

# Проходимся по файлам в папке (без подпапок)
for item in folder.iterdir():
    if not item.is_file(): # "Эта строка в дальнейшем избавляет, от необходимости прописывать  is_file, все предметы и так будут файлами"
        continue
    print('Найден файл:', item.name)

    files_counter['проверенно'] += 1 # Считаем общее колличество проверенных файлов

    # Проходимся по датам, узнаем сколько времени прошло от изменения файла
    file_mtime = item.stat().st_mtime
    file_time = datetime.datetime.fromtimestamp(file_mtime)
    now = datetime.datetime.now()
    age = (now - file_time).days
    print(f'Файл {item.name} был создан {age} назад') # item.name берем из цикла выше

    # Проверяем возраст файла, если он подходит, перемещаем в папку 'архив'
    if age > days_limit:
        shutil.move(str(item), str(archive_folder / item.name))
        files_counter['перемещено'] += 1 # Считаем сколько файлов было перемещено
        print(f'Файл {item.name} перемещен в архив')
        logging.info(f'Файл {item.name} перемещен в архив')

    # Если файл не перемещается в архив счётчик 'оставленных' файлов прибавляется
    else:
         files_counter['оставленно'] += 1

logging.info(f'Итог: проверено {files_counter["проверенно"]}, '
             f'перемещено {files_counter["перемещено"]}, '
             f'оставлено {files_counter["оставленно"]}')

print()
print('=== Отчёт ===')
print(f"Проверено файлов: {files_counter['проверенно']}")
print(f"Перемещено в архив: {files_counter['перемещено']}")
print(f"Оставлено: {files_counter['оставленно']}")