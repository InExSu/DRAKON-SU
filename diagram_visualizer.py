import sys
import yaml
from PyQt5.QtWidgets import (QApplication, QMainWindow, QGraphicsScene, QGraphicsView,
                           QGraphicsRectItem, QGraphicsTextItem, QGraphicsLineItem,
                           QVBoxLayout, QWidget, QPushButton, QFileDialog)
from PyQt5.QtCore import Qt, QRectF, QPointF

class DiagramStateMachine:
    """Машина состояний для обработки диаграмм"""
    def __init__(self):
        self.states = {
            'start': self._draw_start_node,
            'end': self._draw_end_node,
            'condition': self._draw_condition_node,
            'action': self._draw_action_node
        }
    
    def process_node(self, node, scene):
        """Обрабатывает узел диаграммы"""
        handler = self.states.get(node['type'])
        if handler:
            handler(node, scene)
    
    def _draw_start_node(self, node, scene):
        """Рисует стартовый узел"""
        rect = QGraphicsRectItem(QRectF(node['pos'][0], node['pos'][1], 100, 50))
        rect.setBrush(Qt.green)
        scene.addItem(rect)
        self._add_text(node, scene)

    def _draw_end_node(self, node, scene):
        """Рисует конечный узел"""
        rect = QGraphicsRectItem(QRectF(node['pos'][0], node['pos'][1], 100, 50))
        rect.setBrush(Qt.red)
        scene.addItem(rect)
        self._add_text(node, scene)

    def _draw_condition_node(self, node, scene):
        """Рисует условный узел"""
        diamond = self._create_diamond(node['pos'])
        diamond.setBrush(Qt.yellow)
        scene.addItem(diamond)
        self._add_text(node, scene)

    def _draw_action_node(self, node, scene):
        """Рисует узел действия"""
        rect = QGraphicsRectItem(QRectF(node['pos'][0], node['pos'][1], 100, 50))
        rect.setBrush(Qt.blue)
        scene.addItem(rect)
        self._add_text(node, scene)

    def _add_text(self, node, scene):
        """Добавляет текст к узлу"""
        text = QGraphicsTextItem(node['text'])
        text.setPos(node['pos'][0] + 10, node['pos'][1] + 15)
        scene.addItem(text)

    def _create_diamond(self, pos):
        """Создает ромб для условных узлов"""
        diamond = QGraphicsPolygonItem()
        points = [
            QPointF(pos[0] + 50, pos[1]),
            QPointF(pos[0] + 100, pos[1] + 25),
            QPointF(pos[0] + 50, pos[1] + 50),
            QPointF(pos[0], pos[1] + 25)
        ]
        diamond.setPolygon(points)
        return diamond

class DiagramVisualizer(QMainWindow):
    """Главное окно визуализатора"""
    def __init__(self):
        super().__init__()
        self.state_machine = DiagramStateMachine()
        self.init_ui()
    
    def init_ui(self):
        """Инициализация интерфейса"""
        self.setWindowTitle("DRAKON Visualizer")
        self.setGeometry(100, 100, 800, 600)
        
        # Создание сцены и представления
        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene, self)
        
        # Кнопки управления
        self.load_btn = QPushButton("Загрузить YAML", self)
        self.load_btn.clicked.connect(self.load_yaml)
        
        # Настройка лейаута
        central_widget = QWidget(self)
        layout = QVBoxLayout()
        layout.addWidget(self.load_btn)
        layout.addWidget(self.view)
        central_widget.setLayout(layout)
        
        self.setCentralWidget(central_widget)
    
    def load_yaml(self):
        """Загружает YAML файл"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Открыть файл DRAKON", "", "YAML Files (*.yaml *.yml)")
        
        if file_path:
            self.scene.clear()
            with open(file_path, 'r') as file:
                data = yaml.safe_load(file)
                self.render_diagram(data)
    
    def render_diagram(self, data):
        """Отрисовывает диаграмму из данных"""
        for function in data['functions'].values():
            for node in function['nodes']:
                # Добавляем позицию для каждого узла
                node['pos'] = (50 + node['id'] * 120, 50 + node['id'] * 120)
                self.state_machine.process_node(node, self.scene)

def main():
    app = QApplication(sys.argv)
    visualizer = DiagramVisualizer()
    visualizer.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()