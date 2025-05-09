import sys
import yaml
from PyQt5.QtWidgets import (QApplication, QMainWindow, QGraphicsScene, QGraphicsView,
                           QGraphicsRectItem, QGraphicsTextItem, QGraphicsLineItem,
                           QVBoxLayout, QWidget, QPushButton, QFileDialog)
from PyQt5.QtCore import Qt, QRectF, QPointF

# Функции для отрисовки узлов диаграммы
def draw_start_node(node, scene):
    """Отрисовывает стартовый узел"""
    rect = QGraphicsRectItem(QRectF(node['pos'][0], node['pos'][1], 100, 50))
    rect.setBrush(Qt.green)
    scene.addItem(rect)
    add_text(node, scene)

def draw_end_node(node, scene):
    """Отрисовывает конечный узел"""
    rect = QGraphicsRectItem(QRectF(node['pos'][0], node['pos'][1], 100, 50))
    rect.setBrush(Qt.red)
    scene.addItem(rect)
    add_text(node, scene)

def draw_condition_node(node, scene):
    """Отрисовывает условный узел"""
    diamond = create_diamond(node['pos'])
    diamond.setBrush(Qt.yellow)
    scene.addItem(diamond)
    add_text(node, scene)

def draw_action_node(node, scene):
    """Отрисовывает узел действия"""
    rect = QGraphicsRectItem(QRectF(node['pos'][0], node['pos'][1], 100, 50))
    rect.setBrush(Qt.blue)
    scene.addItem(rect)
    add_text(node, scene)

def add_text(node, scene):
    """Добавляет текст к узлу"""
    text = QGraphicsTextItem(node['text'])
    text.setPos(node['pos'][0] + 10, node['pos'][1] + 15)
    scene.addItem(text)

def create_diamond(pos):
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

# Основные функции приложения
def init_ui(window):
    """Инициализирует интерфейс приложения"""
    window.setWindowTitle("DRAKON Visualizer")
    window.setGeometry(100, 100, 800, 600)
    
    # Создание сцены и представления
    scene = QGraphicsScene(window)
    view = QGraphicsView(scene, window)
    
    # Кнопки управления
    load_btn = QPushButton("Загрузить YAML", window)
    
    # Настройка лейаута
    central_widget = QWidget(window)
    layout = QVBoxLayout()
    layout.addWidget(load_btn)
    layout.addWidget(view)
    central_widget.setLayout(layout)
    
    window.setCentralWidget(central_widget)
    
    return scene, view, load_btn

def load_yaml(scene):
    """Загружает YAML файл и запускает отрисовку"""
    file_path, _ = QFileDialog.getOpenFileName(
        None, "Открыть файл DRAKON", "", "YAML Files (*.yaml *.yml)")
    
    if file_path:
        scene.clear()
        with open(file_path, 'r') as file:
            documents = list(yaml.safe_load_all(file))
            combined_data = {}
            for doc in documents:
                if doc:
                    combined_data.update(doc)
            render_diagram(combined_data, scene)

def render_diagram(data, scene):
    """Отрисовывает диаграмму из данных"""
    if 'functions' not in data:
        return
        
    y_pos = 50
    
    for function_name, function_data in data['functions'].items():
        if 'nodes' not in function_data:
            continue
            
        x_pos = 50
        
        # Добавляем заголовок функции
        text = QGraphicsTextItem(function_name)
        text.setPos(x_pos, y_pos - 30)
        scene.addItem(text)
        
        # Отрисовываем узлы
        for node in function_data['nodes']:
            node['pos'] = (x_pos, y_pos)
            draw_node(node, scene)
            y_pos += 120
            
        y_pos += 100

def draw_node(node, scene):
    """Выбирает и вызывает соответствующую функцию отрисовки узла"""
    node_handlers = {
        'start': draw_start_node,
        'end': draw_end_node,
        'condition': draw_condition_node,
        'action': draw_action_node
    }
    
    handler = node_handlers.get(node['type'])
    if handler:
        handler(node, scene)

def main():
    """Точка входа в приложение"""
    app = QApplication(sys.argv)
    window = QMainWindow()
    
    scene, view, load_btn = init_ui(window)
    load_btn.clicked.connect(lambda: load_yaml(scene))
    
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()