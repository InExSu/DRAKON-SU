from PyQt5.QtWidgets import (QApplication, QMainWindow, QGraphicsScene, QGraphicsView,
                            QGraphicsRectItem, QGraphicsTextItem, QGraphicsLineItem,
                            QToolBar, QAction, QDockWidget, QListWidget, QLineEdit,
                            QVBoxLayout, QWidget, QLabel)
from PyQt5.QtCore import Qt, QRectF, QLineF
import sys
from PyQt5.QtWidgets import QStyle

# Функции для создания элементов интерфейса
def create_toolbar(window):
    """Создает панель инструментов"""
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
    dock.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)
    
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

def main():
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle("DRAKON SU diagram")
    window.setGeometry(100, 100, 800, 600)
    
    # Создание элементов интерфейса
    toolbar = create_toolbar(window)
    function_dock, filter_input, function_list = create_function_list(window)
    scene, view = create_diagram_canvas(window)
    
    # Настройка и отображение
    setup_layout(window, toolbar, function_dock, view)
    draw_sample_diagram(scene)
    
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()