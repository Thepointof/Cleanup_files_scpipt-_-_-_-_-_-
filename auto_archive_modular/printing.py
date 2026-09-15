def hello_message(folder_path, days_limit):
    print('Я запустился!')
    print('Аргументы которе мне передали', folder_path, days_limit)
    

def finding_message(name):
    print('Найден файл:', name)
    

def time_message(name, age):
    print(f'Файл {name} был создан {age} дней назад') # item.name берем из цикла выше
    

def repo(counter):
    print()
    print('=== Отчёт ===')
    print(f"Проверено файлов: {counter['проверенно']}")
    print(f"Перемещено в архив: {counter['перемещено']}")
    print(f"Оставлено: {counter['оставленно']}")

def moved_mes(name):
    print(f'Файл {name} перемещен в архив')
