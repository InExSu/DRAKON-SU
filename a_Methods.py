import csv
from datetime import datetime
import os

def log_2_csv(message, level = "Info", file_name="log.csv"):
    
    frame = inspect.currentframe().f_back  # Переход к предыдущему фрейму (вызывающему)
    function_name = frame.f_code.co_name     # Имя функции
    del frame  # Рекомендуется удалять вручную из-за возможных циклов ссылок
    
    # Проверяем, существует ли файл
    file_exists = os.path.isfile(file_name)
    
    # Открываем файл на дозапись
    with open(file_name, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

        # Если файл новый — пишем заголовки
        if not file_exists:
            writer.writerow(['Timestamp', 'Function', 'Level', 'Message'])

        # Записываем строку лога
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        writer.writerow([timestamp, function_name, level.upper(), message])
        
        
import os
import shutil
import csv

def file_CSV_Crop(s_File_Name, i_MegaByte):
    """
    Усекает CSV-файл до заданного размера в МЕГАБАЙТАХ,
    оставляя заголовок без изменений.
    
    :param s_File_Name: Имя CSV-файла
    :param i_MegaByte: Целевой размер файла в мегабайтах
    :return: True — если обрезка выполнена, False — иначе
    """
    target_bytes = i_MegaByte * 1024 * 1024  # Переводим МБ в байты
    file_size = os.path.getsize(s_File_Name)

    if file_size <= target_bytes:
        # print(f"[INFO] Файл {s_File_Name} уже меньше или равен {i_MegaByte} МБ.")
        return False

    # print(f"[INFO] Начинаем обрезку файла {s_File_Name} до {i_MegaByte} МБ...")

    temp_file = s_File_Name + ".tmp"

    with open(s_File_Name, 'r', newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        headers = next(reader)  # Сохраняем заголовки

        rows = []
        for row in reader:
            rows.append(row)

        # Подсчитываем сколько строк нужно удалить, чтобы уложиться в лимит
        while len(rows) > 0:
            with open(temp_file, 'w', newline='', encoding='utf-8') as outfile:
                writer = csv.writer(outfile)
                writer.writerow(headers)
                writer.writerows(rows)
            if os.path.getsize(temp_file) <= target_bytes:
                break
            rows.pop(0)  # Удаляем самую старую запись (первую строку после заголовка)

    # Заменяем исходный файл на обработанный
    shutil.move(temp_file, s_File_Name)
    # print(f"[OK] Обрезка завершена. Файл {s_File_Name} теперь меньше {i_MegaByte} МБ.")
    return True