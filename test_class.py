from PyQt5.QtWidgets import (QApplication, QMainWindow, QGraphicsScene, QGraphicsView, 
                            QGraphicsRectItem, QGraphicsTextItem, QGraphicsLineItem, 
                            QToolBar, QAction, QDockWidget, QListWidget, QLineEdit, 
                            QVBoxLayout, QWidget)
from PyQt5.QtCore import Qt, QRectF, QLineF
import sys
from PyQt5.QtWidgets import QLabel


class DiagramWindow(QMainWindow):
    def __init__(self):
        """Инициализация главного окна"""
        super().__init__()
        self.setWindowTitle("DRAKON SUC diagram")
        self.setGeometry(100, 100, 800, 600)
        
        # Создаем плавающую панель инструментов
        self.create_toolbar()
        
        # Создаем плавающий список элементов
        self.create_element_list()
        
        # Создаем сцену и вид
        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene, self)
        self.setCentralWidget(self.view)
        
        # Рисуем элементы диаграммы
        # self.draw_diagram()

    def create_toolbar(self):
        """Создание вертикальной панели инструментов справа от списка элементов"""
        toolbar = QToolBar(self)
        toolbar.setMovable(True)
        toolbar.setOrientation(Qt.Vertical)  # Устанавливаем вертикальную ориентацию
        
        # Добавляем заголовок
        title_label = QLabel("Инструменты")
        title_label.setStyleSheet("font-weight: bold; padding: 5px;")
        toolbar.addWidget(title_label)
        
        # Добавляем разделитель
        toolbar.addSeparator()
        
        # Добавляем действия на панель
        new_action = QAction("Новый", self)
        open_action = QAction("Открыть", self)
        save_action = QAction("Сохранить", self)
        
        toolbar.addAction(new_action)
        toolbar.addAction(open_action)
        toolbar.addAction(save_action)
        
        # Размещаем справа от списка элементов
        self.addToolBar(Qt.LeftToolBarArea, toolbar)

    def create_element_list(self):
        """Создание плавающего списка элементов с фильтрацией"""
        # Создаем док-виджет
        dock = QDockWidget("Функции", self)
        dock.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)
        
        # Создаем контейнер для виджетов
        container = QWidget()
        layout = QVBoxLayout()
        
        # Поле фильтрации
        self.filter_input = QLineEdit()
        self.filter_input.setPlaceholderText("Фильтр")
        self.filter_input.textChanged.connect(self.filter_elements)
        layout.addWidget(self.filter_input)
        
        # Список элементов
        self.element_list = QListWidget()
        self.element_list.addItems(["Прямоугольник", "Ромб", "Овал", "Линия", "Текст"])
        layout.addWidget(self.element_list)
        
        container.setLayout(layout)
        dock.setWidget(container)
        
        # Размещаем слева
        self.addDockWidget(Qt.LeftDockWidgetArea, dock)

    def filter_elements(self):
        """Фильтрация элементов списка"""
        filter_text = self.filter_input.text().lower()
        for i in range(self.element_list.count()):
            item = self.element_list.item(i)
            item.setHidden(filter_text not in item.text().lower())

    def draw_diagram(self):
        """Метод для рисования диаграммы"""
        # Первый прямоугольник с текстом
        rect1 = QGraphicsRectItem(QRectF(50, 50, 100, 50))
        rect1.setBrush(Qt.white)
        self.scene.addItem(rect1)
        
        text1 = QGraphicsTextItem("01")
        text1.setPos(85, 65)
        self.scene.addItem(text1)
        
        # Второй прямоугольник с текстом
        rect2 = QGraphicsRectItem(QRectF(50, 150, 100, 50))
        rect2.setBrush(Qt.white)
        self.scene.addItem(rect2)
        
        text2 = QGraphicsTextItem("02")
        text2.setPos(85, 165)
        self.scene.addItem(text2)
        
        # Линия между прямоугольниками
        line = QGraphicsLineItem(QLineF(100, 100, 100, 150))
        self.scene.addItem(line)


def main():
    """Основная функция приложения"""
    app = QApplication(sys.argv)
    window = DiagramWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()