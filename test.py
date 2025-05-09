from PyQt5.QtWidgets import (QApplication, QMainWindow, QGraphicsScene, QGraphicsView, 
                             QGraphicsRectItem, QGraphicsTextItem, QGraphicsLineItem, 
                             QToolBar, QAction, QDockWidget, QListWidget, QLineEdit, 
                             QVBoxLayout, QWidget, QLabel)
from PyQt5.QtCore import Qt, QRectF, QLineF
import sys
from PyQt5.QtWidgets import QStyle


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DRAKON SU diagram")
        self.setGeometry(100, 100, 800, 600)

        # Инициализация интерфейса
        self.init_ui()

    def init_ui(self):
        # 1. Создаем панель инструментов (слева)
        self.create_toolbar()

        # 2. Создаем холст диаграмм (центр)
        self.create_diagram_canvas()

        # 3. Создаем панель функций (справа)
        self.create_function_list()

        # Дополнительные настройки интерфейса
        self.setup_layout()

    def create_toolbar(self):
        """Создание вертикальной панели инструментов (левая часть)"""
        self.toolbar = QToolBar("Инструменты", self)
        self.toolbar.setMovable(False)
        self.toolbar.setOrientation(Qt.Vertical)

        # Заголовок
        title_label = QLabel("Инструменты")
        title_label.setStyleSheet("font-weight: bold; padding: 5px;")
        self.toolbar.addWidget(title_label)
        self.toolbar.addSeparator()

        # Добавляем действия с иконками
        file_action = QAction(self.style().standardIcon(
            QStyle.SP_FileIcon), "Файлы", self)
        file_action.triggered.connect(self.toggle_file_tools)
        self.toolbar.addAction(file_action)

        # Размещаем слева
        self.addToolBar(Qt.LeftToolBarArea, self.toolbar)

    def create_function_list(self):
        """Создание док-панели со списком функций (правая часть)"""
        self.function_dock = QDockWidget("Функции", self)
        self.function_dock.setFeatures(
            QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)

        container = QWidget()
        layout = QVBoxLayout()

        # Поле фильтрации
        self.filter_input = QLineEdit()
        self.filter_input.setPlaceholderText("Фильтр функций...")
        self.filter_input.textChanged.connect(self.filter_functions)
        layout.addWidget(self.filter_input)

        # Список функций
        self.function_list = QListWidget()
        self.function_list.addItems(
            ["header", "function_01", "function_02", "footer"])
        layout.addWidget(self.function_list)

        container.setLayout(layout)
        self.function_dock.setWidget(container)

        # Размещаем справа
        self.addDockWidget(Qt.RightDockWidgetArea, self.function_dock)

    def create_diagram_canvas(self):
        """Создание центрального холста для диаграмм"""
        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene, self)
        self.setCentralWidget(self.view)

        # Пример диаграммы
        self.draw_sample_diagram()

    def setup_layout(self):
        """Настройка расположения элементов интерфейса"""
        # Устанавливаем ширину панелей
        self.function_dock.setFixedWidth(200)
        self.toolbar.setFixedWidth(150)

        # Разделяем панель инструментов и функций
        self.insertToolBarBreak(self.toolbar)

    def toggle_file_tools(self):
        """Переключение видимости дополнительных инструментов"""
        if not hasattr(self, 'file_tools'):
            self.create_file_tools()

        if self.file_tools.isVisible():
            self.file_tools.hide()
        else:
            self.file_tools.show()

    def create_file_tools(self):
        """Создание дополнительной панели инструментов для файлов"""
        self.file_tools = QToolBar("Файловые операции", self)
        self.file_tools.setOrientation(Qt.Vertical)

        # Добавляем действия
        actions = [
            ("Создать", "SP_FileDialogNewFolder"),
            ("Открыть", "SP_DialogOpenButton"),
            ("Сохранить", "SP_DialogSaveButton")
        ]

        for text, icon in actions:
            action = QAction(self.style().standardIcon(
                getattr(QStyle, icon)), text, self)
            if text == "Создать":
                action.triggered.connect(self.create_new_file)
            self.file_tools.addAction(action)

        # Размещаем справа от основной панели инструментов
        self.addToolBar(Qt.LeftToolBarArea, self.file_tools)

    def create_new_file(self):
        """Создание нового файла .drakon_SU"""
        from PyQt5.QtWidgets import QFileDialog
        
        # Открываем диалог сохранения файла
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Создать новый файл",
            "",
            "DRAKON Files (*.drakon_SU)"
        )
        
        if file_path:
            # Добавляем расширение, если его нет
            if not file_path.endswith('.drakon_SU'):
                file_path += '.drakon_SU'
            
            # Создаем файл с базовой структурой
            with open(file_path, 'w') as f:
                f.write('{\n    "type": "drakon",\n    "items": {}\n}')

    def filter_functions(self):
        """Фильтрация списка функций"""
        filter_text = self.filter_input.text().lower()
        for i in range(self.function_list.count()):
            item = self.function_list.item(i)
            item.setHidden(filter_text not in item.text().lower())

    def draw_sample_diagram(self):
        """Рисование тестовой диаграммы"""
        rect1 = QGraphicsRectItem(QRectF(50, 50, 100, 50))
        rect1.setBrush(Qt.white)
        self.scene.addItem(rect1)

        text1 = QGraphicsTextItem("Start")
        text1.setPos(75, 65)
        self.scene.addItem(text1)

        rect2 = QGraphicsRectItem(QRectF(50, 150, 100, 50))
        rect2.setBrush(Qt.white)
        self.scene.addItem(rect2)

        text2 = QGraphicsTextItem("End")
        text2.setPos(80, 165)
        self.scene.addItem(text2)

        line = QGraphicsLineItem(QLineF(100, 100, 100, 150))
        self.scene.addItem(line)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()