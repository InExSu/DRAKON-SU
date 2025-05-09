from PyQt5.QtWidgets import (QApplication, QMainWindow, QGraphicsScene, QGraphicsView, 
                            QGraphicsRectItem, QGraphicsTextItem, QGraphicsLineItem, 
                            QToolBar, QAction, QDockWidget, QListWidget, QLineEdit, 
                            QVBoxLayout, QWidget)
from PyQt5.QtCore import Qt, QRectF, QLineF
import sys
from PyQt5.QtWidgets import QLabel

def create_toolbar(window):
    """Создание вертикальной панели инструментов справа от списка элементов"""
    toolbar = QToolBar(window)
    toolbar.setMovable(True)
    toolbar.setOrientation(Qt.Vertical)
    
    title_label = QLabel("Инструменты")
    title_label.setStyleSheet("font-weight: bold; padding: 5px;")
    toolbar.addWidget(title_label)
    
    toolbar.addSeparator()
    
    new_action = QAction("Новый", window)
    open_action = QAction("Открыть", window)
    save_action = QAction("Сохранить", window)
    
    toolbar.addAction(new_action)
    toolbar.addAction(open_action)
    toolbar.addAction(save_action)
    
    window.addToolBar(Qt.LeftToolBarArea, toolbar)

def create_element_list(window):
    """Создание плавающего списка элементов с фильтрацией"""
    dock = QDockWidget("Функции", window)
    dock.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)
    
    container = QWidget()
    layout = QVBoxLayout()
    
    filter_input = QLineEdit()
    filter_input.setPlaceholderText("Фильтр")
    filter_input.textChanged.connect(lambda: filter_elements(filter_input, element_list))
    layout.addWidget(filter_input)
    
    element_list = QListWidget()
    element_list.addItems(["Прямоугольник", "Ромб", "Овал", "Линия", "Текст"])
    layout.addWidget(element_list)
    
    container.setLayout(layout)
    dock.setWidget(container)
    
    window.addDockWidget(Qt.LeftDockWidgetArea, dock)

def filter_elements(filter_input, element_list):
    """Фильтрация элементов списка"""
    filter_text = filter_input.text().lower()
    for i in range(element_list.count()):
        item = element_list.item(i)
        item.setHidden(filter_text not in item.text().lower())

def draw_diagram(scene):
    """Метод для рисования диаграммы"""
    rect1 = QGraphicsRectItem(QRectF(50, 50, 100, 50))
    rect1.setBrush(Qt.white)
    scene.addItem(rect1)
    
    text1 = QGraphicsTextItem("01")
    text1.setPos(85, 65)
    scene.addItem(text1)
    
    rect2 = QGraphicsRectItem(QRectF(50, 150, 100, 50))
    rect2.setBrush(Qt.white)
    scene.addItem(rect2)
    
    text2 = QGraphicsTextItem("02")
    text2.setPos(85, 165)
    scene.addItem(text2)
    
    line = QGraphicsLineItem(QLineF(100, 100, 100, 150))
    scene.addItem(line)

def main():
    """Основная функция приложения"""
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle("DRAKON SUC diagram")
    window.setGeometry(100, 100, 800, 600)
    
    create_toolbar(window)
    create_element_list(window)
    
    scene = QGraphicsScene(window)
    view = QGraphicsView(scene, window)
    window.setCentralWidget(view)
    
    draw_diagram(scene)
    
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()