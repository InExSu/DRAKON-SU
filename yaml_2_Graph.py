import sys
import yaml
from PyQt5.QtWidgets import (QApplication, QMainWindow, QGraphicsScene, QGraphicsView,
                           QGraphicsRectItem, QGraphicsTextItem, QGraphicsLineItem,
                           QGraphicsPolygonItem, QVBoxLayout, QWidget, QPushButton, QFileDialog)
from PyQt5.QtCore import Qt, QRectF, QPointF, QLineF
from PyQt5.QtGui import QPolygonF  # Добавлен правильный импорт

# Функции для отрисовки узлов диаграммы
def draw_start_node(node, scene):
    """Отрисовывает стартовый узел"""
    rect = QGraphicsRectItem(QRectF(node['pos'][0], node['pos'][1], 100, 50))
    # Убрана установка цвета заливки
    scene.addItem(rect)
    add_text(node, scene)

def draw_end_node(node, scene):
    """Отрисовывает конечный узел"""
    rect = QGraphicsRectItem(QRectF(node['pos'][0], node['pos'][1], 100, 50))
    # Убрана установка цвета заливки
    scene.addItem(rect)
    add_text(node, scene)

def draw_condition_node(node, scene):
    """Отрисовывает условный узел"""
    diamond = create_diamond(node['pos'])
    # Убрана установка цвета заливки
    scene.addItem(diamond)
    add_text(node, scene)

def draw_action_node(node, scene):
    """Отрисовывает узел действия"""
    rect = QGraphicsRectItem(QRectF(node['pos'][0], node['pos'][1], 100, 50))
    # Убрана установка цвета заливки
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
    points = QPolygonF([
        QPointF(pos[0] + 50, pos[1]),
        QPointF(pos[0] + 100, pos[1] + 25),
        QPointF(pos[0] + 50, pos[1] + 50),
        QPointF(pos[0], pos[1] + 25)
    ])
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

def get_node_geometry(node, x_pos, y_pos):
    """Возвращает геометрию узла в зависимости от типа"""
    if node['type'] == 'condition':
        return {
            'left': (x_pos + 25, y_pos + 25),
            'right': (x_pos + 75, y_pos + 25),
            'main': (x_pos + 50, y_pos + 50)
        }
    return (x_pos + 50, y_pos + 50)

def update_positions(node, x_pos, y_pos):
    """Обновляет позиции для следующего узла"""
    if node['type'] == 'condition' and isinstance(node.get('connections'), list):
        return (x_pos + 200, y_pos)
    return (50, y_pos + 120)

def get_start_point(node, nodes_dict, i):
    """Возвращает начальную точку соединения"""
    if node['type'] == 'condition':
        return nodes_dict[node['id']]['left'] if i == 0 else nodes_dict[node['id']]['right']
    src_x, src_y = node['pos']
    return (src_x + 50, src_y + 50)

def get_end_point(target_id, nodes_dict):
    """Возвращает точку соединения - середину верхней стороны нижней фигуры"""
    if isinstance(nodes_dict[target_id], dict):
        # Для ромба используем нижнюю точку
        return nodes_dict[target_id]['main']
    # Для прямоугольников: середина верхней стороны (X+50, Y)
    return (nodes_dict[target_id][0], nodes_dict[target_id][1])

def draw_connections(nodes, nodes_dict, scene):
    """Отрисовывает все соединения между узлами одной функции"""
    for node in nodes:
        if not node.get('connections'):
            continue
            
        connections = list(node['connections'].values()) if isinstance(node['connections'], dict) else node['connections']
        
        for i, target_id in enumerate(connections):
            # Проверяем, что целевой узел принадлежит текущей функции
            if not any(n['id'] == target_id for n in nodes):
                continue
                
            start_point = get_start_point(node, nodes_dict, i)
            end_point = get_end_point(target_id, nodes_dict)
            draw_connection(start_point, end_point, scene)

def render_diagram(data, scene):
    """Отрисовывает диаграмму из данных с соединениями"""
    if not data.get('functions'):
        return
        
    y_pos = 50
    
    for function_name, function_data in data['functions'].items():
        if not function_data.get('nodes'):
            continue
            
        # Отрисовка заголовка функции
        text = QGraphicsTextItem(function_name)
        text.setPos(50, y_pos - 30)
        scene.addItem(text)
        
        # Отрисовка узлов и соединений
        nodes_dict = {}
        x_pos = 50
        for node in function_data['nodes']:
            node['pos'] = (x_pos, y_pos)
            draw_node(node, scene)
            
            # Сохраняем геометрию узла
            nodes_dict[node['id']] = get_node_geometry(node, x_pos, y_pos)
            
            # Обновляем позиции
            x_pos, y_pos = update_positions(node, x_pos, y_pos)
            
        # Отрисовка соединений
        draw_connections(function_data['nodes'], nodes_dict, scene)
        
        y_pos += 100

def draw_connection(start_pos, end_pos, scene):
    """Отрисовывает линию соединения между узлами"""
    line = QGraphicsLineItem(QLineF(start_pos[0], start_pos[1], end_pos[0], end_pos[1]))
    scene.addItem(line)

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