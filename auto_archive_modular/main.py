from prep import get_args, is_folder_exist, prepare_archive, log_in_folder
from printing import hello_message, finding_message, time_message, repo, moved_mes
import sys
import datetime
import shutil
import logging
from pathlib import Path

if __name__ == "__main__":
   
    folder_path, days_limit = get_args()
    folder = is_folder_exist(folder_path)
    archive = prepare_archive(folder)
    log_is_in_folder = log_in_folder(folder)

    logging.basicConfig(filename=str(log_is_in_folder), level=logging.INFO, format='%(asctime)s - %(message)s') # создаем лог о проделанной работе

    logging.info(f'Запуск мониторинга папки {folder_path}, лимит {days_limit} дней') # выводим сообщение лога

    hello_message(folder_path, days_limit)

    files_counter = {'перемещено': 0, 'оставленно': 0, 'проверенно': 0} # Словарь со счётчиком файлов

    # Проходимся по файлам в папке (без подпапок)
    for item in folder.iterdir():
        if not item.is_file(): # "Эта строка в дальнейшем избавляет, от необходимости прописывать  is_file, все предметы и так будут файлами"
            continue
        finding_message(item.name)
        files_counter['проверенно'] += 1 # Считаем общее колличество проверенных файлов

        # Проходимся по датам, узнаем сколько времени прошло от изменения файла
        file_mtime = item.stat().st_mtime
        file_time = datetime.datetime.fromtimestamp(file_mtime)
        now = datetime.datetime.now()
        age = (now - file_time).days
        time_message(item.name, age)

        # Проверяем возраст файла, если он подходит, перемещаем в папку 'архив'
        if age > days_limit:
            shutil.move(str(item), str(archive / item.name))
            files_counter['перемещено'] += 1 # Считаем сколько файлов было перемещено
            moved_mes(item.name)
            logging.info(f'Файл {item.name} перемещен в архив')

        # Если файл не перемещается в архив счётчик 'оставленных' файлов прибавляется
        else:
            files_counter['оставленно'] += 1
    repo(files_counter)

    logging.info(f'Итог: проверено {files_counter["проверенно"]}, '
                f'перемещено {files_counter["перемещено"]}, '
                f'оставлено {files_counter["оставленно"]}')

