from PyQt5.QtWidgets import (QApplication, QGraphicsView, QGraphicsScene,
                             QMainWindow, QDialog, QVBoxLayout, QPushButton,
                             QButtonGroup, QWidget, QLineEdit, QComboBox,
                             QToolBar, QLabel, QAction, QDockWidget, QListWidget,
                             QGraphicsRectItem, QGraphicsTextItem, QGraphicsLineItem,
                             QGraphicsPolygonItem, QStyle)
from PyQt5.QtCore import QRectF, QPointF, Qt, QLineF
from PyQt5.QtWidgets import QFileDialog
import sys


def file_Choice(files_Opened):
    """Функция выбора файла или действия"""
    dialog = QDialog()
    dialog.setWindowTitle("Выберите действие")
    layout = QVBoxLayout()

    # Создаем группу кнопок для управления выбором
    button_group = QButtonGroup()

    # Кнопка "Файл создать"
    btn_create = QPushButton("Файл создать")
    button_group.addButton(btn_create, 1)  # ID 1
    layout.addWidget(btn_create)

    # Кнопка "Файл открыть"
    btn_open = QPushButton("Файл открыть")
    button_group.addButton(btn_open, 2)  # ID 2
    layout.addWidget(btn_open)

    # Кнопки для ранее открытых файлов
    for i, file in enumerate(files_Opened, start=3):
        btn_file = QPushButton(file)
        button_group.addButton(btn_file, i)  # ID начинаются с 3
        layout.addWidget(btn_file)

    # Кнопка "Выход"
    btn_exit = QPushButton("Выход")
    button_group.addButton(btn_exit, 0)  # ID 0
    layout.addWidget(btn_exit)

    # Настраиваем диалог
    dialog.setLayout(layout)
    result = "Exit"  # По умолчанию возвращаем Exit

    # Обработчик нажатия кнопок
    def button_clicked(id):
        """Обработчик нажатия кнопок диалога"""
        nonlocal result
        action_map = {
            0: "Exit",
            1: "File create",
            2: "File open dialog"
        }
        result = action_map.get(id, files_Opened[id - 3] if id >= 3 else None)
        dialog.accept()

    button_group.buttonClicked[int].connect(button_clicked)

    dialog.exec_()

    return result


def create_process(x, y, width, height, text, scene):
    """Создает прямоугольник процесса"""
    rect = scene.addRect(QRectF(x, y, width, height))
    text_item = scene.addText(text)
    text_item.setPos(x + 10, y + 10)
    return rect


def create_condition(x, y, size, text, scene):
    from PyQt5.QtWidgets import QGraphicsPolygonItem
    from PyQt5.QtCore import QPointF

    # Создаем точки ромба
    points = [
        QPointF(x, y - size / 2),       # верхняя
        QPointF(x + size / 2, y),       # правая
        QPointF(x, y + size / 2),       # нижняя
        QPointF(x - size / 2, y)        # левая
    ]

    # Создаем и добавляем ромб на сцену
    diamond = QGraphicsPolygonItem()
    diamond.setPolygon(points)
    scene.addItem(diamond)

    # Добавляем текст
    text_item = scene.addText(text)
    text_item.setPos(x - text_item.boundingRect().width() / 2,
                     y - text_item.boundingRect().height() / 2)

    return diamond


def create_main_window():
    """Создает и настраивает главное окно приложения"""
    window = QMainWindow()
    window.setWindowTitle("DRAKON SU diagram")
    window.setGeometry(100, 100, 800, 600)

    return window


def code_Good(s_Code):
    """Проверяет код на корректность"""
    # TODO : реализовать
    return True


def file_Open_Dialog():
    """Открывает диалоговое окно выбора файла

    Returns:
        str: Путь к выбранному файлу или None, если выбор отменен
    """
    from PyQt5.QtWidgets import QFileDialog

    # Настройки диалога
    options = QFileDialog.Options()
    # Для более стабильной работы на MacOS
    options |= QFileDialog.DontUseNativeDialog

    # Открываем диалог выбора файла
    file_path, _ = QFileDialog.getOpenFileName(
        None,  # Родительское окно
        "Выберите файл",  # Заголовок
        "",  # Начальная директория
        "All Files (*);;Python Files (*.drakon)",  # Фильтры файлов
        options=options
    )

    return file_path if file_path else None


def create_toolbar(window):
    """Создает панель инструментов для главного окна"""
    toolbar = QToolBar("Инструменты", window)
    toolbar.setMovable(False)
    toolbar.setOrientation(Qt.Vertical)

    title_label = QLabel("Инструменты")
    title_label.setStyleSheet("font-weight: bold; padding: 5px;")
    toolbar.addWidget(title_label)
    toolbar.addSeparator()

    file_action = QAction(window.style().standardIcon(
        QStyle.SP_FileIcon), "Файлы", window)
    toolbar.addAction(file_action)

    return toolbar


def create_function_list(window, a1_Functions):
    """Создает список функций"""
    dock = QDockWidget("Функции", window)
    dock.setFeatures(QDockWidget.DockWidgetMovable |
                     QDockWidget.DockWidgetFloatable)

    container = QWidget()
    layout = QVBoxLayout()

    filter_input = QLineEdit()
    filter_input.setPlaceholderText("Фильтр функций...")
    layout.addWidget(filter_input)

    function_list = QListWidget()
    function_list.addItems(a1_Functions)
    layout.addWidget(function_list)

    container.setLayout(layout)
    dock.setWidget(container)

    return dock, filter_input, function_list


def create_diagram_canvas(window):
    """Создает холст для диаграмм"""
    scene = QGraphicsScene(window)
    view = QGraphicsView(scene, window)
    return scene, view


def setup_layout(window, toolbar, dock, view):
    """Настраивает расположение элементов"""
    dock.setFixedWidth(200)
    toolbar.setFixedWidth(150)
    window.setCentralWidget(view)
    window.addToolBar(Qt.LeftToolBarArea, toolbar)
    window.addDockWidget(Qt.RightDockWidgetArea, dock)


def yaml_Validate(s_YAML: str) -> bool:
    # Проверяет валидность YAML-кода
    import yaml
    try:
        yaml.safe_load(s_YAML)
        return True
    except yaml.YAMLError:
        return False


def file_New_Create():
    # TODO протестируй
    """Создает шаблон нового файла DRAKON в формате YAML"""
    s_Code = """
header: |
functions:
  - name: "reName"
    params: ""
    return_type: ""
    icons:
      - id: 1
        type: "Header"
        text: "reName"
        connections:
            right:
                target: 2
            down:
                target: 4
      - id: 2
        type: "Params"
        text: "n: int"
        connections:
            right:
                target: 3
      - id: 3
        type: "Type"
        text: "-> int"
      - id: 4
        type: "End"
        text: "Конец"
footer: |
"""

    # сохранить s_Code в файл
    s_File_Name = QFileDialog.getSaveFileName(
        None, "Сохранить файл", "", "DRAKON Files (*.drakon)")[0]
    if s_File_Name:
        with open(s_File_Name, "w") as file:
            file.write(s_Code)
        return s_File_Name
    else:
        return ""


def commandLine_parse(s):
    """Парсинг строки командной строки в словарь опций
    Args:
        s (str): Строка командной строки
    Returns:
        dict: Словарь {опция: значение}
    """
    import re
    tokens = re.findall(r'(?:[^\s"]|"(?:\\.|[^"])*")+', s)
    args = {}
    i = 0
    while i < len(tokens):
        token = tokens[i]
        # Обработка long опций (--option)
        if token.startswith('--'):
            key = token[2:]
            if '=' in key:
                key, val = key.split('=', 1)
                args[key] = val.strip('"')
            elif i + 1 < len(tokens) and not tokens[i + 1].startswith('-'):
                args[key] = tokens[i + 1].strip('"')
                i += 1
            else:
                args[key] = True
        # Обработка short опций (-o)
        elif token.startswith('-'):
            key = token[1:]
            if i + 1 < len(tokens) and not tokens[i + 1].startswith('-'):
                args[key] = tokens[i + 1].strip('"')
                i += 1
            else:
                args[key] = True
        i += 1
    return args


def options_FileName():
    """Обработка опций командной строки"""

    s_Options = " ".join(sys.argv[1:])
    options = commandLine_parse(s_Options)

    s_File_Name = options.get("file_open", "")

    return s_File_Name

import yaml

def yaml_Functions(s_Code):
    """
    Извлекает все имена функций из YAML-структуры.
    
    Args:
        s_Code (str): YAML-строка с описанием функций
        
    Returns:
        list: Список имен функций или пустой список при ошибке
    """
    try:
        data = yaml.safe_load(s_Code)
        if not isinstance(data, dict):
            return []
        return [func['name'] for func in data.get('functions', []) 
                if isinstance(func, dict) and 'name' in func]
    except (yaml.YAMLError, AttributeError):
        return []