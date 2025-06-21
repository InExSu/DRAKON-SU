import shutil
import csv
from datetime import datetime
import inspect
import os
import tempfile
from PyQt5.QtWidgets import QApplication, QMessageBox


def log_2_CSV(message, level="Info", file_name="log.csv"):

    # Переход к предыдущему фрейму (вызывающему)
    frame = inspect.currentframe().f_back
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
            # Удаляем самую старую запись (первую строку после заголовка)
            rows.pop(0)

    # Заменяем исходный файл на обработанный
    shutil.move(temp_file, s_File_Name)
    # print(f"[OK] Обрезка завершена. Файл {s_File_Name} теперь меньше {i_MegaByte} МБ.")
    return True


def silhouette_Code():
    return '''{
        "items": {
            "1": {
                "type": "end"
            },
            "2": {
                "type": "branch",
                "branchId": 1,
                "one": "3",
                "content": "<p>Start</p>"
            },
            "3": {
                "type": "branch",
                "content": "<p>Exit</p>",
                "one": "1",
                "branchId": 2
            }
        },
        "type": "drakon",
        "id": "user_Action_Processing.drakon"
    }'''


def primitive_Code():
#     return '''{
#     "type": "drakon",
#     "items": {}
# }'''
    # return '''
    #     digraph drakon_diagram {
    #         rankdir=TB;

    #         node_1 [label="Начало", shape=ellipse, fillcolor="#4C8BF5", style=filled, fontcolor=white];
    #         node_2 [label="Конец", shape=ellipse, fillcolor="#4C8BF5", style=filled, fontcolor=white];

    #         node_1 -> node_2;
    #     }
    #     '''
    return '''{
        "type": "drakon",
        "items": {
            "1": {
                "type": "start",
                "content": "Начало"
            },
            "2": {
                "type": "end",
                "content": "Конец"
            }
        }
    }'''
    
def file_Name_Temp(suffix=".tmp"):
    """
    Создает временный файл с заданным суффиксом и возвращает его путь.
    В случае ошибки возвращает пустую строку.
    """
    try:
        # Создаем временный файл
        fd, temp_path = tempfile.mkstemp(suffix=suffix)
        os.close(fd)  # Закрываем дескриптор файла
        return temp_path
    except Exception as e:
        print(f"[Ошибка] Не удалось создать временный файл: {e}")
        return ""


def warning_Show(s_Message):
        # Переход к предыдущему фрейму (вызывающему)
    frame = inspect.currentframe().f_back
    function_name = frame.f_code.co_name     # Имя функции
    del frame  # Рекомендуется удалять вручную из-за возможных циклов ссылок
    
    app = QApplication([])  # Создаём приложение (нужно для GUI)
    
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Information)
    msg_box.setWindowTitle("Информация")
    msg_box.setText(s_Message)
    msg_box.setStandardButtons(QMessageBox.Ok)
    
    msg_box.exec_()  # Отображаем окно и ждём нажатия кнопки


def file_Create(s_File_Name):
    """
    Создаёт пустой файл по указанному пути.
    Автоматически создаёт отсутствующие папки.
    Возвращает True при успехе, False при ошибке.
    """
    try:
        # Получаем директорию файла
        directory = os.path.dirname(s_File_Name)

        # Если директория указана и не существует — создаём её
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        # Создаём пустой файл
        with open(s_File_Name, 'w', encoding='utf-8', newline='') as file:
            pass  # Открытие в режиме 'w' уже создаёт файл

        # Проверяем, действительно ли файл был создан
        if not os.path.isfile(s_File_Name):
            print(f"[Ошибка] Файл '{s_File_Name}' не был создан.")
            return False

        return True

    except Exception as e:
        return False


def file_Check(s_File_Name):
    # Проверяем, существует ли файл
    file_exists = os.path.isfile(s_File_Name)

def diagram_Show(s_DOT_Code):
    """
    Отображает диаграмму на основе строки с DOT-кодом.

    :param s_DOT_Code: строка с DOT-описанием графа
    """
    try:
        # Создаем объект графа из переданного DOT-кода
        src = Source(s_DOT_Code)

        # Генерируем изображение и отображаем его
        src.view()
        
        return True
    
    except Exception as e:
        print(f"[Ошибка] Не удалось отобразить диаграмму: {e}")
        return False
    
def wait_for_keypress(a1_Keys):
    """
    Ждёт нажатия клавиши и возвращает её имя.
    """
    while True:
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            key = event.name.lower()
            if key in a1_Keys:
                return key
