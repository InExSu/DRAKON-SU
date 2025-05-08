"""
Рендерер DRAKON диаграмм с использованием PyQt5
"""
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsRectItem, QGraphicsTextItem, QGraphicsPolygonItem
from PyQt5.QtCore import Qt, QRectF, QPointF

class DrakonRenderer:
    def __init__(self):
        self.scene = QGraphicsScene()
        self.node_types = {
            'action': self.render_action,
            'branch': self.render_branch,
            'case': self.render_case,
            'question': self.render_question,
            'select': self.render_select
        }
        self.x_step = 200
        self.y_step = 100
        self.connector_style = {
            'color': Qt.black,
            'width': 2,
            'arrow_size': 10
        }

    def render_action(self, node, x, y):
        """Отрисовка блока действия"""
        rect = QGraphicsRectItem(QRectF(x, y, 180, 60))
        rect.setBrush(Qt.white)
        self.scene.addItem(rect)
        
        text = QGraphicsTextItem(node.get('content', ''))
        text.setPos(x + 10, y + 20)
        self.scene.addItem(text)
        return x, y + self.y_step

    def render_branch(self, node, x, y):
        """Отрисовка ветвления"""
        diamond = QGraphicsPolygonItem()
        points = QPolygonF([
            QPointF(x, y - 30),
            QPointF(x + 40, y),
            QPointF(x, y + 30),
            QPointF(x - 40, y)
        ])
        diamond.setPolygon(points)
        self.scene.addItem(diamond)
        
        text = QGraphicsTextItem(node.get('content', ''))
        text.setPos(x - text.boundingRect().width()/2, y - 15)
        self.scene.addItem(text)
        return x, y + self.y_step

    def render_case(self, node, x, y):
        """Отрисовка вариантов выбора"""
        # Реализация аналогична render_branch
        return x, y + self.y_step

    def render_question(self, node, x, y):
        """Отрисовка условия"""
        # Реализация аналогична render_branch
        return x, y + self.y_step

    def render_select(self, node, x, y):
        """Отрисовка выбора"""
        # Реализация аналогична render_branch
        return x, y + self.y_step

    def draw_connectors(self, from_node, to_nodes):
        """Отрисовка соединительных линий между узлами"""
        start_point = QPointF(from_node['x'] + 90, from_node['y'] + 30)
        
        for connection in to_nodes:
            if not connection['target']:
                continue
                
            end_node = self.nodes[connection['target']]
            end_point = QPointF(end_node['x'] + 90, end_node['y'])
            
            path = QGraphicsPathItem()
            path.setPen(QPen(QColor(self.connector_style['color']), 
                           self.connector_style['width']))
            
            path_line = QPainterPath(start_point)
            path_line.lineTo(end_point.x(), end_point.y())
            path.setPath(path_line)
            
            # Добавление стрелки
            arrow = QGraphicsPolygonItem()
            arrow.setBrush(QColor(self.connector_style['color']))
            arrow.setPolygon(QPolygonF([
                QPointF(0, 0),
                QPointF(-5, 10),
                QPointF(5, 10)
            ]))
            arrow.setPos(end_point)
            arrow.setRotation(-90)
            
            self.scene.addItem(path)
            self.scene.addItem(arrow)

    def render_diagram(self, nodes):
        """Основной метод отрисовки с учетом связей"""
        self.nodes = nodes  # Сохраняем данные узлов
        x, y = 50, 50
        for node_id, node in nodes.items():
            render_func = self.node_types.get(node['type'])
            if render_func:
                x, y = render_func(node, x, y)
        
        # Отрисовка связей после всех элементов
        for node_id, node_data in nodes.items():
            if node_data['connections']:
                self.draw_connectors(node_data, node_data['connections'])
        
        return self.scene