"""
Парсер файлов DRAKON формата (.drakon)
"""
import json

def parse_drakon_file(file_path):
    """
    Парсит DRAKON файл и возвращает структуру данных
    
    Args:
        file_path (str): Путь к файлу .drakon
        
    Returns:
        dict: Словарь с элементами диаграммы
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if 'items' not in data:
        raise ValueError("Invalid DRAKON file format")
    
    nodes = {}
    
    # Добавляем обработку связей между элементами
    for item_id, item_data in data['items'].items():
        node = {
            'id': item_id,
            'type': item_data['type'],
            'content': item_data.get('content', ''),
            'connections': []
        }
        
        # Собираем связи для разных типов элементов
        if item_data['type'] in ['branch', 'question', 'case']:
            node['connections'] = [
                {'target': item_data.get('one'), 'label': 'yes'},
                {'target': item_data.get('two'), 'label': 'no'}
            ]
        elif 'one' in item_data:
            node['connections'].append({'target': item_data['one'], 'label': ''})
            
        nodes[item_id] = node
    
    return nodes