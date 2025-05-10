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


def draw_sample_diagram(scene):
    #  Удалить
    """Рисует тестовую диаграмму"""
    rect1 = QGraphicsRectItem(QRectF(50, 50, 100, 50))
    rect1.setBrush(Qt.white)
    scene.addItem(rect1)

    text1 = QGraphicsTextItem("Start")
    text1.setPos(75, 65)
    scene.addItem(text1)

    rect2 = QGraphicsRectItem(QRectF(50, 150, 100, 50))
    rect2.setBrush(Qt.white)
    scene.addItem(rect2)

    text2 = QGraphicsTextItem("End")
    text2.setPos(80, 165)
    scene.addItem(text2)

    line = QGraphicsLineItem(QLineF(100, 100, 100, 150))
    scene.addItem(line)

def code_2_Graph(s_Code):
    """Преобразует YAML-код в графическое представление диаграммы"""
    import yaml
    from PyQt5.QtWidgets import QGraphicsScene
    from PyQt5.QtCore import QRectF, QLineF
    from PyQt5.QtGui import QPainterPath, QPen, QBrush, QColor

    scene = QGraphicsScene()
    
    try:
        data = yaml.safe_load(s_Code)
        if not data or 'functions' not in data:
            return scene

        y_offset = 50

        for func_name, func_data in data['functions'].items():
            if 'nodes' not in func_data:
                continue

            node_items = {}
            x_pos = 50

            for node in func_data['nodes']:
                node_id = node['id']
                node_type = node['type']
                text = node.get('text', '')
                item = None

                if node_type == 'start':
                    # Создаем скругленный прямоугольник через Path
                    path = QPainterPath()
                    path.addRoundedRect(QRectF(x_pos, y_offset, 100, 40), 10, 10)
                    item = scene.addPath(path, QPen(Qt.black), QBrush(QColor(200, 255, 200)))
                    
                    text_item = scene.addText(text)
                    text_item.setPos(x_pos + 25, y_offset + 10)
                    y_offset += 60

                elif node_type == 'end':
                    path = QPainterPath()
                    path.addRoundedRect(QRectF(x_pos, y_offset, 100, 40), 10, 10)
                    item = scene.addPath(path, QPen(Qt.black), QBrush(QColor(255, 200, 200)))
                    
                    text_item = scene.addText(text)
                    text_item.setPos(x_pos + 25, y_offset + 10)
                    y_offset += 60

                if item:
                    node_items[node_id] = (item, x_pos, y_offset)

            # Отрисовка связей между узлами
            for node in func_data['nodes']:
                if 'connections' in node and node['connections']:
                    source_id = node['id']
                    if source_id not in node_items:
                        continue

                    source_item, src_x, src_y = node_items[source_id]
                    source_bottom = src_y - 60 + 40  # Нижняя точка стартового узла

                    for target_id in node['connections']:
                        if target_id not in node_items:
                            continue

                        target_item, trg_x, trg_y = node_items[target_id]
                        target_top = trg_y - 60  # Верхняя точка целевого узла

                        # Рисуем вертикальную линию соединения
                        line = scene.addLine(
                            QLineF(src_x + 50, source_bottom, 
                                  trg_x + 50, target_top),
                            QPen(QColor(0, 0, 0), 1)
                        )

        # Удаляем строки с view и масштабированием
        scene.setSceneRect(scene.itemsBoundingRect())

    except yaml.YAMLError as e:
        print(f"Ошибка парсинга YAML: {e}")
    
    return scene
