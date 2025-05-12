import logging
import yaml
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtCore import QRectF, QLineF, Qt, QPointF
from PyQt5.QtGui import QPainterPath, QPen, QBrush, QColor, QPolygonF

# Настройка логгера


def setup_logging():
    logging.basicConfig(
        filename='drakon_debug.log',
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

# Конфигурация визуализации


def get_config():
    return {
        'NODE_WIDTH': 150,
        'NODE_HEIGHT': 50,
        'BRANCH_OFFSET': 120,
        'COLORS': {
            'start': QColor(200, 255, 200),
            'end': QColor(255, 200, 200),
            'if': QColor(240, 240, 150),
            'action': QColor(220, 220, 255)
        }
    }

# Парсинг YAML


def parse_yaml(yaml_str: str) -> dict:
    try:
        data = yaml.safe_load(yaml_str)
        if not data or 'functions' not in data:
            logging.error("Invalid YAML structure: missing 'functions'")
            return None
        return data
    except yaml.YAMLError as e:
        logging.error(f"YAML parsing error: {e}")
        return None

# Расчет позиций узлов


def calculate_positions(nodes: list, config: dict) -> dict:
    positions = {}
    y_level = 50

    # Первый проход - базовые позиции
    for node in nodes:
        node_id = str(node['id'])
        positions[node_id] = (400, y_level)
        y_level += 80 if node['type'] != 'end' else 60

    # Второй проход - обработка ветвлений
    for node in nodes:
        if node['type'] == 'if':
            process_if_branch(node, positions, config)

    return positions


def process_if_branch(node: dict, positions: dict, config: dict):
    connections = node.get('connections', [])
    valid_targets = []

    # Обработка разных форматов соединений
    if isinstance(connections, dict):
        connections = [{'target': k, 'direction': v}
                       for k, v in connections.items()]
    elif isinstance(connections, list):
        connections = [{'target': c, 'direction': 'down'} if not isinstance(c, dict) else c 
                       for c in connections]

    # Фильтрация валидных целей
    for conn in connections:
        target = str(conn.get('target', ''))
        if target in positions:
            valid_targets.append((target, conn.get('direction', 'down')))

    # Позиционирование ветвей
    base_x, base_y = positions[str(node['id'])]
    for i, (target, direction) in enumerate(valid_targets):
        x_offset = config['BRANCH_OFFSET'] if direction in [
            'right', 'right-down'] else -config['BRANCH_OFFSET']
        positions[target] = (base_x + x_offset, base_y + 80)

# Отрисовка узлов


def draw_node(scene: QGraphicsScene, node: dict, pos: tuple, config: dict):
    x, y = pos
    node_type = node['type']
    text = node.get('text', '')

    # Создание формы
    if node_type == 'if':
        shape = create_hexagon(
            x, y, config['NODE_WIDTH'], config['NODE_HEIGHT'])
        scene.addPolygon(shape, QPen(Qt.black, 2),
                         QBrush(config['COLORS'][node_type]))
    elif node_type in ['start', 'end']:
        path = QPainterPath()
        path.addRoundedRect(x - config['NODE_WIDTH'] / 2, y, 
                            config['NODE_WIDTH'], config['NODE_HEIGHT'], 10, 10)
        scene.addPath(path, QPen(Qt.black, 2),
                      QBrush(config['COLORS'][node_type]))
    else:
        scene.addRect(x - config['NODE_WIDTH'] / 2, y,
                      config['NODE_WIDTH'], config['NODE_HEIGHT'],
                      QPen(Qt.black, 2), QBrush(config['COLORS'].get(node_type, Qt.white)))

    # Добавление текста
    text_item = scene.addText(text)
    text_item.setPos(x - text_item.boundingRect().width() / 2, y + 10)


def create_hexagon(x: float, y: float, width: float, height: float) -> QPolygonF:
    return QPolygonF([
        QPointF(x - width / 2 + 10, y),
        QPointF(x + width / 2 - 10, y),
        QPointF(x + width / 2, y + height / 2),
        QPointF(x + width / 2 - 10, y + height),
        QPointF(x - width / 2 + 10, y + height),
        QPointF(x - width / 2, y + height / 2)
    ])

# Отрисовка соединений


def draw_connections(scene: QGraphicsScene, nodes: list, positions: dict, config: dict):
    for node in nodes:
        source_id = str(node['id'])
        if source_id not in positions:
            continue

        connections = get_normalized_connections(node)

        for conn in connections:
            target_id = str(conn['target'])
            if target_id not in positions:
                continue

            draw_single_connection(scene, node, conn, positions, config)


def get_normalized_connections(node: dict) -> list:
    connections = node.get('connections', [])
    normalized = []

    if isinstance(connections, dict):
        normalized = [{'target': k, 'direction': v}
                      for k, v in connections.items()]
    elif isinstance(connections, list):
        normalized = [c if isinstance(c, dict) else {'target': c, 'direction': 'down'} 
                      for c in connections]
    return normalized


def draw_single_connection(scene: QGraphicsScene, node: dict, conn: dict, 
                           positions: dict, config: dict):
    source_id = str(node['id'])
    target_id = str(conn['target'])
    src_x, src_y = positions[source_id]
    trg_x, trg_y = positions[target_id]
    direction = conn.get('direction', 'down')

    if node['type'] == 'if':
        draw_branch_connection(scene, src_x, src_y, trg_x,
                               trg_y, direction, config)
    else:
        draw_straight_connection(scene, src_x, src_y, trg_x, trg_y, config)


def draw_branch_connection(scene: QGraphicsScene, src_x: float, src_y: float,
                           trg_x: float, trg_y: float, direction: str, config: dict):
    horizontal = 'right' if direction in ['right', 'right-down'] else 'left'
    start_x = src_x + (config['NODE_WIDTH'] / 2 if horizontal ==
                       'right' else -config['NODE_WIDTH'] / 2)
    start_y = src_y + config['NODE_HEIGHT'] / 2

    mid_x = start_x + (50 if horizontal == 'right' else -50)
    mid_y = max(trg_y, src_y + 20)

    path = QPainterPath()
    path.moveTo(start_x, start_y)
    path.lineTo(mid_x, start_y)
    path.lineTo(mid_x, mid_y)
    path.lineTo(trg_x, trg_y)

    pen_color = QColor(
        0, 150, 0) if horizontal == 'right' else QColor(150, 0, 0)
    scene.addPath(path, QPen(pen_color, 2))


def draw_straight_connection(scene: QGraphicsScene, src_x: float, src_y: float,
                             trg_x: float, trg_y: float, config: dict):
    line = QLineF(src_x, src_y + config['NODE_HEIGHT'], trg_x, trg_y)
    scene.addLine(line, QPen(Qt.black, 2))

# Главная функция


def code_2_Graph(yaml_str: str, function_name: str = None) -> QGraphicsScene:
    setup_logging()
    config = get_config()
    scene = QGraphicsScene()

    try:
        data = parse_yaml(yaml_str)
        if not data:
            return scene

        # Выбор функции
        functions = data['functions']
        function_name = function_name or next(iter(functions))
        nodes = functions[function_name].get('nodes', [])

        if not nodes:
            logging.error("No nodes to display")
            return scene

        # Расчет и отрисовка
        positions = calculate_positions(nodes, config)

        for node in nodes:
            node_id = str(node['id'])
            if node_id in positions:
                draw_node(scene, node, positions[node_id], config)

        draw_connections(scene, nodes, positions, config)

    except Exception as e:
        logging.error(f"Visualization error: {str(e)}")

    return scene
