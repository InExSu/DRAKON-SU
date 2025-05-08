from PyQt5.QtWidgets import (QApplication, QGraphicsView, QGraphicsScene,
                             QMainWindow, QDialog, QVBoxLayout, QPushButton,
                             QButtonGroup, QWidget, QLineEdit, QComboBox)
from PyQt5.QtCore import QRectF
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
    result = None

    # Обработчик нажатия кнопок
    def button_clicked(id):
        """Обработчик нажатия кнопок диалога"""
        nonlocal result
        action_map = {
            0: "Exit",
            1: "File create",
            2: "File open"
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
        QPointF(x, y - size/2),       # верхняя
        QPointF(x + size/2, y),       # правая
        QPointF(x, y + size/2),       # нижняя
        QPointF(x - size/2, y)        # левая
    ]

    # Создаем и добавляем ромб на сцену
    diamond = QGraphicsPolygonItem()
    diamond.setPolygon(points)
    scene.addItem(diamond)

    # Добавляем текст
    text_item = scene.addText(text)
    text_item.setPos(x - text_item.boundingRect().width()/2,
                     y - text_item.boundingRect().height()/2)

    return diamond


def create_main_window():
    """Создает и настраивает главное окно приложения"""
    window = QMainWindow()
    window.setWindowTitle("DRAKON SUC")
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
    options |= QFileDialog.DontUseNativeDialog  # Для более стабильной работы на MacOS
    
    # Открываем диалог выбора файла
    file_path, _ = QFileDialog.getOpenFileName(
        None,  # Родительское окно
        "Выберите файл",  # Заголовок
        "",  # Начальная директория
        "All Files (*);;Python Files (*.drakon)",  # Фильтры файлов
        options=options
    )
    
    return file_path if file_path else None


def create_search_panel(parent, items_list):
    """Создает панель поиска и фильтрации элементов
    
    Args:
        parent: Родительский виджет
        items_list: Список элементов для отображения
        
    Returns:
        QWidget: Виджет с элементами управления поиском и фильтрацией
    """
    from PyQt5.QtWidgets import QLineEdit, QComboBox, QHBoxLayout
    
    # Создаем контейнер для элементов управления
    search_panel = QWidget(parent)
    layout = QHBoxLayout()
    
    # Поле поиска
    search_field = QLineEdit()
    search_field.setPlaceholderText("Поиск...")
    layout.addWidget(search_field)
    
    # Фильтр по категориям
    filter_combo = QComboBox()
    filter_combo.addItem("Все элементы")
    # Добавляем уникальные категории из items_list
    categories = set(item.get('category', '') for item in items_list if 'category' in item)
    for category in categories:
        filter_combo.addItem(category)
    layout.addWidget(filter_combo)
    
    search_panel.setLayout(layout)
    return search_panel

def filter_items(items, search_text, filter_category):
    """Фильтрует список элементов по тексту и категории
    
    Args:
        items: Список элементов
        search_text: Текст для поиска
        filter_category: Выбранная категория
        
    Returns:
        list: Отфильтрованный список элементов
    """
    filtered = items
    
    # Применяем фильтр по категории
    if filter_category and filter_category != "Все элементы":
        filtered = [item for item in filtered 
                   if item.get('category', '') == filter_category]
    
    # Применяем поиск по тексту
    if search_text:
        search_lower = search_text.lower()
        filtered = [item for item in filtered 
                   if search_lower in str(item).lower()]
    
    return filtered