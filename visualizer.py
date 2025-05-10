import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.lines import Line2D

def visualize_drakon(json_file):
    # Загрузка JSON-файла
    with open(json_file) as f:
        data = json.load(f)
    
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Координаты и размеры элементов
    node_positions = {}
    y_offset = 0
    
    # Отрисовка элементов
    for node in data['nodes']:
        node_id = node['id']
        node_type = node['type']
        text = node['text']
        
        if node_type == 'start':
            # Ромб для старта (xy, numVertices, radius)
            diamond = patches.RegularPolygon(
                (0, -y_offset), numVertices=4, radius=0.5,
                fill=True, color='lightgreen'
            )
            ax.add_patch(diamond)
            ax.text(0, -y_offset, text, ha='center', va='center')
            node_positions[node_id] = (0, -y_offset)
            y_offset += 1.5
            
        elif node_type == 'end':
            # Ромб для конца
            diamond = patches.RegularPolygon(
                (0, -y_offset), numVertices=4, radius=0.5,
                fill=True, color='salmon'
            )
            ax.add_patch(diamond)
            ax.text(0, -y_offset, text, ha='center', va='center')
            node_positions[node_id] = (0, -y_offset)
            y_offset += 1.5
            
        elif node_type == 'condition':
            # Ромб для условия с поворотом
            diamond = patches.RegularPolygon(
                (0, -y_offset), numVertices=4, radius=0.5,
                orientation=0.785,  # 45 градусов в радианах
                fill=True, color='yellow'
            )
            ax.add_patch(diamond)
            ax.text(0, -y_offset, text, ha='center', va='center')
            node_positions[node_id] = (0, -y_offset)
            y_offset += 1.5
            
        elif node_type == 'action':
            # Прямоугольник для действия
            rect = patches.Rectangle(
                (-0.8, -y_offset-0.3), 1.6, 0.6,
                fill=True, color='lightblue'
            )
            ax.add_patch(rect)
            ax.text(0, -y_offset, text, ha='center', va='center')
            node_positions[node_id] = (0, -y_offset)
            y_offset += 1
    
        elif node_type == 'condition':
            # Ромб для условия
            diamond = patches.RegularPolygon(
                (0, -y_offset), 4, 0.5, 45,
                fill=True, color='yellow'
            )
            ax.add_patch(diamond)
            ax.text(0, -y_offset, text, ha='center', va='center')
            node_positions[node_id] = (0, -y_offset)
            y_offset += 1.5
            
        # Добавьте другие типы узлов по аналогии
    
    # Отрисовка связей
    for node in data['nodes']:
        if 'connections' in node and node['connections']:
            start_pos = node_positions[node['id']]
            for conn in node['connections']:
                end_pos = node_positions[conn]
                line = Line2D(
                    [start_pos[0], end_pos[0]], 
                    [start_pos[1], end_pos[1]],
                    lw=1, color='black'
                )
                ax.add_line(line)
    
    plt.tight_layout()
    plt.show()

# Пример JSON-файла для тестирования
sample_json = {
    "nodes": [
        {"id": 1, "type": "start", "text": "Начало", "connections": [2]},
        {"id": 2, "type": "action", "text": "Действие 1", "connections": [3]},
        {"id": 3, "type": "condition", "text": "Условие?", "connections": [4, 5]},
        {"id": 4, "type": "action", "text": "Если да", "connections": [6]},
        {"id": 5, "type": "action", "text": "Если нет", "connections": [6]},
        {"id": 6, "type": "end", "text": "Конец", "connections": []}
    ]
}

# Сохраняем пример в файл
with open('sample.json', 'w') as f:
    json.dump(sample_json, f)

# Визуализация
visualize_drakon('sample.json')