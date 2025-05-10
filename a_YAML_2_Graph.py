import logging
import yaml
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsPolygonItem
from PyQt5.QtCore import QRectF, QLineF, Qt, QPointF
from PyQt5.QtGui import QPainterPath, QPen, QBrush, QColor, QPolygonF

# Конфигурация логирования
logging.basicConfig(
    filename='drakon_debug.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Константы для визуализации
NODE_WIDTH = 150
NODE_HEIGHT = 50
BRANCH_OFFSET = 120
COLORS = {
    'start': QColor(200, 255, 200),
    'end': QColor(255, 200, 200),
    'if': QColor(240, 240, 150),
    'action': QColor(220, 220, 255)
}


def parse_yaml_code(s_code: str) -> dict:
    """Парсит YAML-код и выполняет базовую валидацию структуры."""
    try:
        data = yaml.safe_load(s_code)
        if not data or 'functions' not in data:
            logging.error("Отсутствуют функции в YAML")
            return None

        # Валидация структуры функций
        for func_name, func_data in data['functions'].items():
            if 'nodes' not in func_data:
                logging.error(f"Функция {func_name} не содержит узлов")
                return None
        return data
    except yaml.YAMLError as e:
        logging.error(f"Ошибка парсинга YAML: {e}")
        return None


def calculate_node_positions(nodes: list) -> dict:
    """Вычисляет позиции с учетом вложенных соединений."""
    positions = {}
    y_level = 50
    branch_stack = []

    # Первый проход: создание базовых позиций
    for node in nodes:
        node_id = str(node['id'])
        positions[node_id] = (400, y_level)
        y_level += 80 if node['type'] != 'end' else 60

    # Второй проход: обработка ветвлений с глубоким сканированием
    for node in nodes:
        if node['type'] == 'if':
            connections = node.get('connections', [])
            valid_targets = []

            # Глубокая обработка вложенных словарей
            for conn in connections:
                if isinstance(conn, dict):
                    target = str(conn.get('target', ''))
                    if target and target in positions:
                        valid_targets.append(target)

            # Позиционирование только валидных целей
            base_x, base_y = positions[str(node['id'])]
            for i, target in enumerate(valid_targets):
                x_offset = BRANCH_OFFSET if i == 0 else -BRANCH_OFFSET
                positions[target] = (base_x + x_offset, base_y + 80)

    return positions


def draw_connections(scene: QGraphicsScene, nodes: list, positions: dict):
    """Обрабатывает соединения узлов с учетом сложных структур."""
    for node in nodes:
        source_id = str(node['id'])
        if source_id not in positions:
            continue

        connections = node.get('connections', [])
        processed_connections = []

        # Нормализация формата соединений для словарей с метками
        if isinstance(connections, list):
            for conn in connections:
                if isinstance(conn, dict):
                    target = str(conn.get('target', ''))
                    if target:  # Добавляем только валидные цели
                        processed_connections.append({
                            'target': target,
                            'direction': conn.get('direction', 'down')
                        })
                else:
                    processed_connections.append({
                        'target': str(conn),
                        'direction': 'down'
                    })
        elif isinstance(connections, dict):
            for target, direction in connections.items():
                processed_connections.append(
                    {'target': str(target), 'direction': direction})

        # Отрисовка соединений
        for conn in processed_connections:
            target_id = conn['target']
            if target_id not in positions:
                logging.warning(f"Не удалось найти целевой узел: {target_id}")
                continue

            src_x, src_y = positions[source_id]
            trg_x, trg_y = positions[target_id]
            direction = conn.get('direction', 'down')

            # Определение направления соединения
            horizontal_dir = 'right' if direction in [
                'right', 'right-down'] else 'left'

            if node['type'] == 'if':
                start_point = QPointF(
                    src_x + (NODE_WIDTH / 2 if horizontal_dir ==
                             'right' else -NODE_WIDTH / 2),
                    src_y + NODE_HEIGHT / 2
                )

                mid_x = start_point.x() + (50 if horizontal_dir == 'right' else -50)
                mid_y = max(trg_y, src_y + 20)  # Минимальная высота изгиба

                path = QPainterPath()
                path.moveTo(start_point)
                path.lineTo(mid_x, start_point.y())
                path.lineTo(mid_x, mid_y)
                path.lineTo(trg_x, trg_y)

                pen = QPen(QColor(0, 150, 0) if horizontal_dir ==
                           'right' else QColor(150, 0, 0), 2)
                scene.addPath(path, pen)
            else:
                line = QLineF(src_x, src_y + NODE_HEIGHT, trg_x, trg_y)
                scene.addLine(line, QPen(Qt.black, 2))


def draw_node(scene: QGraphicsScene, node: dict, x: float, y: float):
    """Создает графическое представление узла."""
    node_type = node['type']
    text = node.get('text', '')

    # Общие настройки
    pen = QPen(Qt.black, 2)
    brush = QBrush(COLORS.get(node_type, Qt.white))

    if node_type == 'if':
        # Шестиугольник для условия
        hexagon = create_hexagon(x, y, NODE_WIDTH, NODE_HEIGHT)
        item = scene.addPolygon(hexagon, pen, brush)
    elif node_type in ['start', 'end']:
        # Скругленный прямоугольник
        rect = QRectF(x - NODE_WIDTH / 2, y, NODE_WIDTH, NODE_HEIGHT)
        path = QPainterPath()
        path.addRoundedRect(rect, 10, 10)
        item = scene.addPath(path, pen, brush)
    else:
        # Стандартный прямоугольник
        item = scene.addRect(x - NODE_WIDTH / 2, y,
                             NODE_WIDTH, NODE_HEIGHT, pen, brush)

    # Добавление текста
    text_item = scene.addText(text)
    text_width = text_item.boundingRect().width()
    text_item.setPos(x - text_width / 2, y + 10)
    return item


def create_hexagon(x: float, y: float, width: float, height: float) -> QPolygonF:
    """Создает шестиугольник для узлов типа 'if'."""
    return QPolygonF([
        QPointF(x - width / 2 + 10, y),
        QPointF(x + width / 2 - 10, y),
        QPointF(x + width / 2, y + height / 2),
        QPointF(x + width / 2 - 10, y + height),
        QPointF(x - width / 2 + 10, y + height),
        QPointF(x - width / 2, y + height / 2)
    ])


def code_2_Graph(s_code: str, function_name: str = None) -> QGraphicsScene:
    """Главная функция визуализации с улучшенной обработкой ошибок."""
    scene = QGraphicsScene()

    try:
        data = parse_yaml_code(s_code)
        if not data or 'functions' not in data:
            logging.error("Невалидные данные для визуализации")
            return scene

        function_name = function_name or next(iter(data['functions']))
        func_data = data['functions'][function_name]
        nodes = func_data.get('nodes', [])

        # Проверка наличия узлов
        if not nodes:
            logging.error("Нет узлов для отображения")
            return scene

        positions = calculate_node_positions(nodes)

        # Отрисовка элементов
        for node in nodes:
            node_id = str(node['id'])
            if node_id not in positions:
                logging.warning(f"Не найдена позиция для узла {node_id}")
                continue

            try:
                x, y = positions[node_id]
                draw_node(scene, node, x, y)
            except Exception as e:
                logging.error(f"Ошибка при отрисовке узла {node_id}: {e}")

        draw_connections(scene, nodes, positions)

    except Exception as e:
        logging.error(f"Ошибка визуализации: {str(e)}")

    return scene
