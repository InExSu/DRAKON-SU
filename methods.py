from PyQt5.QtWidgets import (QApplication, QGraphicsView, QGraphicsScene,
                             QMainWindow, QDialog, QVBoxLayout, QPushButton,
                             QButtonGroup, QWidget, QLineEdit, QComboBox,
                             QToolBar, QLabel, QAction, QDockWidget, QListWidget,
                             QGraphicsRectItem, QGraphicsTextItem, QGraphicsLineItem,
                             QGraphicsPolygonItem, QStyle)
from PyQt5.QtCore import QRectF, QPointF, Qt, QLineF
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


def create_main_window_OLD():
    """Создает и настраивает главное окно приложения"""
    window = QMainWindow()
    window.setWindowTitle("DRAKON SU")
    window.resize(800, 600)

    # Создаем графическую сцену и представление
    scene = QGraphicsScene()
    view = QGraphicsView(scene)

    # Настраиваем главный layout
    main_layout = QVBoxLayout()
    main_layout.addWidget(view)

    # Создаем центральный виджет
    central_widget = QWidget()
    central_widget.setLayout(main_layout)
    window.setCentralWidget(central_widget)

    return window, scene


def create_main_window():
    """Создает и настраивает главное окно приложения"""
    window = QMainWindow()
    window.setWindowTitle("DRAKON SU diagram")
    window.setGeometry(100, 100, 800, 600)

    # Создание элементов интерфейса
    toolbar = create_toolbar(window)
    function_dock, filter_input, function_list = create_function_list(window)
    scene, view = create_diagram_canvas(window)

    # Настройка и отображение
    setup_layout(window, toolbar, function_dock, view)

    return window, scene


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


def create_function_list(window):
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
    function_list.addItems(["header", "function_01", "function_02", "footer"])
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
    # произвольный код
functions:
    simplex:
        parameters: ""
        returns: ""
        nodes:
        - id: 1 
            type: "start"
            text: "simplex"
            connections: [2]
        - id: 2 
            type: "end"
            text: "конец"
            connections: []
footer: |
    # Код после функций.
"""

    # сохранить s_Code в файл
    s_File_Name = QFileDialog.getSaveFileName(
        dialog, "Сохранить файл", "", "DRAKON Files (*.drakon)")[0]
    if s_File_Name:
        with open(s_File_Name, "w") as file:
            file.write(s_Code)
        return s_File_Name
    else:
        return ""
