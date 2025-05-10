import logging
import yaml
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtCore import QRectF, QLineF, Qt  # Добавлен импорт Qt
from PyQt5.QtGui import QPainterPath, QPen, QBrush, QColor

# Настройка логирования
logging.basicConfig(
    filename='drakon_debug.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def code_2_Graph(s_Code):
    """
    Преобразует YAML-код в графическое представление диаграммы DRAKON.
    Без машины состояний и логирования.
    """
    import yaml
    from PyQt5.QtWidgets import QGraphicsScene
    from PyQt5.QtCore import QRectF, QLineF, Qt
    from PyQt5.QtGui import QPainterPath, QPen, QBrush, QColor

    scene = QGraphicsScene()
    data = yaml.safe_load(s_Code)
    if not data or 'functions' not in data:
        return scene

    for func_name, func_data in data['functions'].items():
        node_items = {}
        x_pos = 50
        y_offset = 50

        # Сначала рисуем все узлы
        for node in func_data.get('nodes', []):
            node_id = node['id']
            node_type = node['type']
            text = node.get('text', '')

            if node_type == 'start':
                path = QPainterPath()
                path.addRoundedRect(QRectF(x_pos, y_offset, 100, 40), 10, 10)
                item = scene.addPath(path, QPen(Qt.black),
                                     QBrush(QColor(200, 255, 200)))
                text_item = scene.addText(text)
                text_item.setPos(x_pos + 25, y_offset + 10)
            elif node_type == 'end':
                path = QPainterPath()
                path.addRoundedRect(QRectF(x_pos, y_offset, 100, 40), 10, 10)
                item = scene.addPath(path, QPen(Qt.black),
                                     QBrush(QColor(255, 200, 200)))
                text_item = scene.addText(text)
                text_item.setPos(x_pos + 25, y_offset + 10)
            elif node_type == 'action':
                item = scene.addRect(QRectF(x_pos, y_offset, 100, 40))
                text_item = scene.addText(text)
                text_item.setPos(x_pos + 10, y_offset + 10)
            elif node_type == 'if':
                from PyQt5.QtWidgets import QGraphicsPolygonItem
                from PyQt5.QtCore import QPointF
                from PyQt5.QtGui import QPolygonF  # Исправленный импорт
                points = [
                    QPointF(x_pos, y_offset - 20),
                    QPointF(x_pos + 50, y_offset),
                    QPointF(x_pos, y_offset + 20),
                    QPointF(x_pos - 50, y_offset)
                ]
                item = QGraphicsPolygonItem()
                item.setPolygon(QPolygonF(points))
                scene.addItem(item)
                text_item = scene.addText(text)
                text_item.setPos(x_pos - text_item.boundingRect().width() / 2,
                                 y_offset - text_item.boundingRect().height() / 2)
            elif node_type == 'switch':
                from PyQt5.QtWidgets import QGraphicsPolygonItem
                from PyQt5.QtCore import QPointF
                from PyQt5.QtGui import QPolygonF  # Исправленный импорт
                points = [
                    QPointF(x_pos - 50, y_offset),
                    QPointF(x_pos, y_offset - 30),
                    QPointF(x_pos + 50, y_offset),
                    QPointF(x_pos, y_offset + 30)
                ]
                item = QGraphicsPolygonItem()
                item.setPolygon(QPolygonF(points))
                scene.addItem(item)
                text_item = scene.addText(text)
                text_item.setPos(x_pos - text_item.boundingRect().width() / 2,
                                 y_offset - text_item.boundingRect().height() / 2)
            elif node_type == 'parallels':
                item = scene.addRect(QRectF(x_pos, y_offset, 100, 40))
                text_item = scene.addText(text)
                text_item.setPos(x_pos + 10, y_offset + 10)
            else:
                continue

            node_items[node_id] = (item, x_pos, y_offset)
            y_offset += 60

        # Затем рисуем соединения
        for node in func_data.get('nodes', []):
            source_id = node['id']
            if source_id not in node_items or 'connections' not in node:
                continue
            source_item, src_x, src_y = node_items[source_id]
            source_bottom = src_y + 40
            for target_id in node['connections']:
                if target_id not in node_items:
                    continue
                target_item, trg_x, trg_y = node_items[target_id]
                target_top = trg_y
                scene.addLine(
                    QLineF(src_x + 50, source_bottom, trg_x + 50, target_top),
                    QPen(QColor(0, 0, 0), 1)
                )

    return scene


def _draw_connections_state(context):
    """Отрисовка связей между узлами"""
    for node in context['func_data']['nodes']:
        if 'connections' in node and node['connections']:
            _draw_node_connections(context, node)
    return 'PROCESS_FUNCTIONS'


def _error_state(context):
    """Обработка ошибок"""
    print(context['error'])
    return 'END'


def _end_state(context):
    """Завершение работы машины"""
    return 'END'


def draw_start_node(scene, x, y, text):
    """Рисует стартовый узел (прямоугольник со скруглёнными углами, зелёный фон)."""
    path = QPainterPath()
    path.addRoundedRect(QRectF(x, y, 100, 40), 10, 10)
    item = scene.addPath(path, QPen(Qt.black), QBrush(QColor(200, 255, 200)))
    text_item = scene.addText(text)
    text_item.setPos(x + 25, y + 10)
    return item


def draw_end_node(scene, x, y, text):
    """Рисует конечный узел (прямоугольник со скруглёнными углами, красный фон)."""
    path = QPainterPath()
    path.addRoundedRect(QRectF(x, y, 100, 40), 10, 10)
    item = scene.addPath(path, QPen(Qt.black), QBrush(QColor(255, 200, 200)))
    text_item = scene.addText(text)
    text_item.setPos(x + 25, y + 10)
    return item


def draw_action_node(scene, x, y, text):
    """Рисует узел действия (прямоугольник)."""
    rect = scene.addRect(QRectF(x, y, 100, 40))
    text_item = scene.addText(text)
    text_item.setPos(x + 10, y + 10)
    return rect


def draw_if_node(scene, x, y, text):
    """Рисует условный узел (ромб)."""
    from PyQt5.QtWidgets import QGraphicsPolygonItem
    from PyQt5.QtCore import QPointF
    points = [
        QPointF(x, y - 20),
        QPointF(x + 50, y),
        QPointF(x, y + 20),
        QPointF(x - 50, y)
    ]
    diamond = QGraphicsPolygonItem()
    diamond.setPolygon(points)
    scene.addItem(diamond)
    text_item = scene.addText(text)
    text_item.setPos(x - text_item.boundingRect().width() / 2,
                     y - text_item.boundingRect().height() / 2)
    return diamond


def draw_switch_node(scene, x, y, text):
    """Рисует узел выбора (шестиугольник)."""
    from PyQt5.QtWidgets import QGraphicsPolygonItem
    from PyQt5.QtCore import QPointF
    points = [
        QPointF(x - 50, y),
        QPointF(x, y - 30),
        QPointF(x + 50, y),
        QPointF(x, y + 30)
    ]
    hexagon = QGraphicsPolygonItem()
    hexagon.setPolygon(points)
    scene.addItem(hexagon)
    text_item = scene.addText(text)
    text_item.setPos(x - text_item.boundingRect().width() / 2,
                     y - text_item.boundingRect().height() / 2)
    return hexagon


def draw_parallels_node(scene, x, y, text):
    """Рисует узел параллельных процессов (прямоугольник)."""
    rect = scene.addRect(QRectF(x, y, 100, 40))
    text_item = scene.addText(text)
    text_item.setPos(x + 10, y + 10)
    return rect


def _draw_node_connections(context, node):
    """Отрисовка связей для узла с корректным позиционированием"""
    source_id = node['id']
    if source_id not in context['node_items']:
        return

    source_item, src_x, src_y = context['node_items'][source_id]
    # Корректный расчет нижней точки исходного узла
    source_bottom = src_y + 40  # 40 - высота узла

    for target_id in node['connections']:
        if target_id not in context['node_items']:
            continue

        target_item, trg_x, trg_y = context['node_items'][target_id]
        # Корректный расчет верхней точки целевого узла
        target_top = trg_y

        # Рисуем вертикальную линию соединения
        context['scene'].addLine(
            QLineF(src_x + 50, source_bottom, 
                   trg_x + 50, target_top),
            QPen(QColor(0, 0, 0), 1)
        )


def _process_functions_state(context):
    """Обработка функций с сбросом позиций"""
    if not hasattr(context, 'func_index'):
        context['func_index'] = 0
        # Сбрасываем позиции для каждой новой функции
        context['y_offset'] = 50  
        context['x_pos'] = 50

    # Исправление: получаем функции из данных контекста
    functions = context['data'].get('functions', {})

    if context['func_index'] < len(functions):
        logging.debug(
            f"Обработка функции {context['func_index'] + 1}/{len(functions)}")
        func_name, func_data = list(functions.items())[context['func_index']]
        context['func_name'] = func_name
        context['func_data'] = func_data
        context['node_items'] = {}
        context['y_offset'] = 50
        context['x_pos'] = 50
        context['func_index'] += 1
        return 'PROCESS_NODES'
    return 'END'


def _draw_start_node(context, node_id, text):
    """Отрисовка стартового узла с фиксированным смещением"""
    path = QPainterPath()
    path.addRoundedRect(
        QRectF(context['x_pos'], context['y_offset'], 100, 40), 10, 10)
    item = context['scene'].addPath(path, QPen(
        Qt.black), QBrush(QColor(200, 255, 200)))
    text_item = context['scene'].addText(text)
    text_item.setPos(context['x_pos'] + 25, context['y_offset'] + 10)
    # Фиксированное смещение для следующего узла
    context['y_offset'] += 60  
    return item


def code_2_Graph(s_Code):
    """
    Преобразует YAML-код в графическое представление диаграммы DRAKON.
    Без машины состояний и логирования.
    """
    import yaml
    from PyQt5.QtWidgets import QGraphicsScene
    from PyQt5.QtCore import QRectF, QLineF, Qt
    from PyQt5.QtGui import QPainterPath, QPen, QBrush, QColor

    scene = QGraphicsScene()
    data = yaml.safe_load(s_Code)
    if not data or 'functions' not in data:
        return scene

    for func_name, func_data in data['functions'].items():
        node_items = {}
        x_pos = 50
        y_offset = 50

        # Сначала рисуем все узлы
        for node in func_data.get('nodes', []):
            node_id = node['id']
            node_type = node['type']
            text = node.get('text', '')

            if node_type == 'start':
                path = QPainterPath()
                path.addRoundedRect(QRectF(x_pos, y_offset, 100, 40), 10, 10)
                item = scene.addPath(path, QPen(Qt.black),
                                     QBrush(QColor(200, 255, 200)))
                text_item = scene.addText(text)
                text_item.setPos(x_pos + 25, y_offset + 10)
            elif node_type == 'end':
                path = QPainterPath()
                path.addRoundedRect(QRectF(x_pos, y_offset, 100, 40), 10, 10)
                item = scene.addPath(path, QPen(Qt.black),
                                     QBrush(QColor(255, 200, 200)))
                text_item = scene.addText(text)
                text_item.setPos(x_pos + 25, y_offset + 10)
            elif node_type == 'action':
                item = scene.addRect(QRectF(x_pos, y_offset, 100, 40))
                text_item = scene.addText(text)
                text_item.setPos(x_pos + 10, y_offset + 10)
            elif node_type == 'if':
                from PyQt5.QtWidgets import QGraphicsPolygonItem
                from PyQt5.QtCore import QPointF
                from PyQt5.QtGui import QPolygonF  # Исправленный импорт
                points = [
                    QPointF(x_pos, y_offset - 20),
                    QPointF(x_pos + 50, y_offset),
                    QPointF(x_pos, y_offset + 20),
                    QPointF(x_pos - 50, y_offset)
                ]
                item = QGraphicsPolygonItem()
                item.setPolygon(QPolygonF(points))
                scene.addItem(item)
                text_item = scene.addText(text)
                text_item.setPos(x_pos - text_item.boundingRect().width() / 2,
                                 y_offset - text_item.boundingRect().height() / 2)
            elif node_type == 'switch':
                from PyQt5.QtWidgets import QGraphicsPolygonItem
                from PyQt5.QtCore import QPointF
                from PyQt5.QtGui import QPolygonF  # Исправленный импорт
                points = [
                    QPointF(x_pos - 50, y_offset),
                    QPointF(x_pos, y_offset - 30),
                    QPointF(x_pos + 50, y_offset),
                    QPointF(x_pos, y_offset + 30)
                ]
                item = QGraphicsPolygonItem()
                item.setPolygon(QPolygonF(points))
                scene.addItem(item)
                text_item = scene.addText(text)
                text_item.setPos(x_pos - text_item.boundingRect().width() / 2,
                                 y_offset - text_item.boundingRect().height() / 2)
            elif node_type == 'parallels':
                item = scene.addRect(QRectF(x_pos, y_offset, 100, 40))
                text_item = scene.addText(text)
                text_item.setPos(x_pos + 10, y_offset + 10)
            else:
                continue

            node_items[node_id] = (item, x_pos, y_offset)
            y_offset += 60

        # Затем рисуем соединения
        for node in func_data.get('nodes', []):
            source_id = node['id']
            if source_id not in node_items or 'connections' not in node:
                continue
            source_item, src_x, src_y = node_items[source_id]
            source_bottom = src_y + 40
            for target_id in node['connections']:
                if target_id not in node_items:
                    continue
                target_item, trg_x, trg_y = node_items[target_id]
                target_top = trg_y
                scene.addLine(
                    QLineF(src_x + 50, source_bottom, trg_x + 50, target_top),
                    QPen(QColor(0, 0, 0), 1)
                )

    return scene
