# Заготовка для преобразования в ДРАКОН схему

# Импорт необходимых модулей для работы приложения
import sys
import json
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsTextItem, QMessageBox, QInputDialog
from PyQt5.QtGui import QPainter, QPen, QBrush, QFont
from PyQt5.QtCore import Qt, QRectF


# --- Инициализация состояния ---
def init_state_data():
    """
    Возвращает словарь, содержащий всё состояние программы.
    Это позволяет обойтись без классов и сохранить данные в одном месте.
    """
    return {
        'json_data': None,
        'element_list': [],
        'link_list': [],
        'indicator_list': [],
        'scene': None,
        'view': None,
        'app': None,
        'current_state': "idle",
        'event': None,
        'selected_indicator': None,
        'transition_table': [],
        'filter_prefix': "",
        'filename': ""
    }


# --- Рисование элемента ---
def element_draw(painter, item):
    """
    Функция отрисовки одного элемента диаграммы (например, начальный, конечный, процесс).
    Позиционирование, цвета, текст — всё берётся из данных элемента.
    """
    painter.save()
    if item['type'] == "start":
        brush = QBrush(Qt.blue)
        pen = QPen(Qt.white, 2)
        painter.setBrush(brush)
        painter.setPen(pen)
        painter.drawRoundedRect(
            item['x'], item['y'], item['width'], item['height'], item['radius'], item['radius'])
    elif item['type'] == "end":
        brush = QBrush(Qt.red)
        pen = QPen(Qt.white, 2)
        painter.setBrush(brush)
        painter.setPen(pen)
        painter.drawRoundedRect(
            item['x'], item['y'], item['width'], item['height'], item['radius'], item['radius'])
    else:
        brush = QBrush(Qt.lightGray)
        pen = QPen(Qt.black, 2)
        painter.setBrush(brush)
        painter.setPen(pen)
        painter.drawRect(item['x'], item['y'], item['width'], item['height'])
    # Цвет текста зависит от типа элемента
    painter.setPen(Qt.white if item['type'] in ["start", "end"] else Qt.black)
    painter.setFont(QFont("Arial", 10))
    text_rect = QRectF(item['x'], item['y'], item['width'], item['height'])
    painter.drawText(text_rect, Qt.AlignCenter, item['content'])
    painter.restore()


# --- Отрисовка фона ---
def draw_foreground(state_data, painter, rect):
    """
    Эта функция рисует связи между элементами и сами элементы на сцене.
    Она вызывается автоматически системой PyQt при перерисовке сцены.
    """
    # Рисуем связи (линии между элементами)
    pen = QPen(Qt.black, 2)
    painter.setPen(pen)
    for link in state_data['link_list']:
        a = link['start']
        b = link['end']
        painter.drawLine(
            a['x'] + a['width'] // 2,
            a['y'] + a['height'],
            b['x'] + b['width'] // 2,
            b['y']
        )
    # Рисуем элементы
    for element in state_data['element_list']:
        element_draw(painter, element)


# --- Загрузка JSON ---
def scene_load_json(state_data):
    """
    Загружает данные из JSON-файла и создаёт список элементов и связей.
    Элементы позиционируются по вертикали друг под другом.
    """
    data = state_data['json_data']
    items_data = data.get("items", {})
    y = 50
    element_list = []
    for item_id, info in items_data.items():
        item_type = info.get("type")
        content = info.get("content", "")
        x = info.get("x", 100)
        y = info.get("y", y)
        element_list.append({
            'id': item_id,
            'type': item_type,
            'content': content,
            'x': x,
            'y': y,
            'width': 120,
            'height': 60,
            'radius': 20
        })
        y += 100
    state_data['element_list'] = element_list

    # Создание связей между элементами (по порядку)
    link_list = []
    for i in range(len(element_list) - 1):
        link_list.append({
            'start': element_list[i],
            'end': element_list[i + 1]
        })
    state_data['link_list'] = link_list


# --- Индикаторы ---
def clear_indicators(state_data):
    """
    Удаляет все индикаторы (o1, l1 и т.п.) с графической сцены.
    """
    for ind in state_data['indicator_list']:
        state_data['scene'].removeItem(ind)
    state_data['indicator_list'].clear()


def add_indicators(state_data):
    """
    Добавляет индикаторы к каждому элементу и связи.
    oX — объектные индикаторы для элементов, lX — линейные для связей.
    """
    clear_indicators(state_data)
    font = QFont("Arial", 10)
    for idx, item in enumerate(state_data['element_list']):
        indicator = QGraphicsTextItem(f"o{idx + 1}")
        indicator.setFont(font)
        indicator.setDefaultTextColor(Qt.darkGreen)
        indicator.setPos(item['x'] + item['width'] + 5,
                         item['y'] + item['height'] // 3)
        state_data['scene'].addItem(indicator)
        state_data['indicator_list'].append(indicator)

    for idx, link in enumerate(state_data['link_list']):
        start = link['start']
        end = link['end']
        tx = (start['x'] + start['width'] // 2 +
              end['x'] + end['width'] // 2) // 2
        ty = (start['y'] + start['height'] + end['y']) // 2
        indicator = QGraphicsTextItem(f"l{idx + 1}")
        indicator.setFont(font)
        indicator.setDefaultTextColor(Qt.darkRed)
        indicator.setPos(tx, ty)
        state_data['scene'].addItem(indicator)
        state_data['indicator_list'].append(indicator)


def filter_indicators(state_data, prefix):
    """
    Отображает только те индикаторы, которые начинаются с заданного префикса (например, o или l).
    """
    clear_indicators(state_data)
    font = QFont("Arial", 10)
    for idx, item in enumerate(state_data['element_list']):
        indicator_id = f"o{idx + 1}"
        if indicator_id.startswith(prefix):
            indicator = QGraphicsTextItem(indicator_id)
            indicator.setFont(font)
            indicator.setDefaultTextColor(Qt.darkGreen)
            indicator.setPos(item['x'] + item['width'] + 5,
                             item['y'] + item['height'] // 3)
            state_data['scene'].addItem(indicator)
            state_data['indicator_list'].append(indicator)

    for idx, link in enumerate(state_data['link_list']):
        indicator_id = f"l{idx + 1}"
        if indicator_id.startswith(prefix):
            start = link['start']
            end = link['end']
            tx = (start['x'] + start['width'] // 2 +
                  end['x'] + end['width'] // 2) // 2
            ty = (start['y'] + start['height'] + end['y']) // 2
            indicator = QGraphicsTextItem(indicator_id)
            indicator.setFont(font)
            indicator.setDefaultTextColor(Qt.darkRed)
            indicator.setPos(tx, ty)
            state_data['scene'].addItem(indicator)
            state_data['indicator_list'].append(indicator)


# --- Обработка событий ---
def process_event(state_data):
    """
    Обрабатывает текущее событие согласно таблице переходов состояний.
    Если найдено совпадение, выполняется действие и изменяется состояние.
    """
    for row in state_data['transition_table']:
        current_state, current_event, new_state, action = row
        if state_data['current_state'] == current_state and state_data['event'] == current_event:
            state_data['current_state'] = new_state
            if action:
                action(state_data)
            state_data['event'] = None
            return


# --- Меню ---
def show_menu(state_data, selected_id):
    """
    Отображает контекстное меню для выбранного индикатора.
    Предоставляет возможность редактирования текста.
    """
    menu = QMessageBox()
    menu.setWindowTitle("Действие")
    menu.setText(f"Выбран {selected_id}")
    btn_edit = menu.addButton("Редактировать текст", QMessageBox.YesRole)
    btn_format = menu.addButton("Формат", QMessageBox.NoRole)
    btn_cancel = menu.addButton("Отмена", QMessageBox.RejectRole)
    result = menu.exec_()
    clicked_button = menu.clickedButton()
    if clicked_button == btn_edit:
        state_data['selected_indicator'] = selected_id
        state_data['current_state'] = "action_menu"
        state_data['event'] = "menu_edit_text"
        process_event(state_data)
    elif clicked_button == btn_format:
        print("Форматирование не реализовано — можно добавить позже")
    else:
        state_data['current_state'] = "edit_mode"


def edit_selected_text(state_data):
    """
    Вызывает диалоговое окно для изменения текста элемента.
    После ввода обновляется содержимое элемента.
    """
    if not state_data.get('selected_indicator'):
        return
    indicator_number = int(state_data['selected_indicator'][1:]) - 1
    if state_data['selected_indicator'].startswith("o"):
        target_element = state_data['element_list'][indicator_number]
    elif state_data['selected_indicator'].startswith("l"):
        target_element = state_data['link_list'][indicator_number]['start']
    else:
        return
    new_text, ok = QInputDialog.getText(None, "Редактировать текст", "Введите новый текст:",
                                        text=target_element['content'])
    if ok and new_text:
        target_element['content'] = new_text
        state_data['event'] = "text_edited"
        process_event(state_data)
    else:
        state_data['current_state'] = "edit_mode"


def redraw_diagram(state_data):
    """
    Перерисовывает диаграмму после редактирования текста.
    """
    state_data['scene'].update()


# --- Сохранение JSON ---
def save_to_json_file(state_data, filename="updated_diagram.json"):
    """
    Сохраняет текущее состояние диаграммы в файл формата JSON.
    """
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(state_data['json_data'], f, ensure_ascii=False, indent=4)
        print(f"[OK] Диаграмма сохранена в {filename}")
    except Exception as e:
        print(f"[Ошибка] Не удалось сохранить файл: {e}")


# --- Таблица переходов ---
def init_transition_table(state_data, filename):
    """
    Инициализирует FSM (Finite State Machine) — таблицу состояний и возможных действий.
    """
    state_data['filename'] = filename
    state_data['transition_table'] = [
        ("idle", "key_F", "edit_mode", lambda s: add_indicators(s)),
        ("edit_mode", "key_o", "selecting_o", lambda s: filter_indicators(s, "o")),
        ("edit_mode", "key_l", "selecting_l", lambda s: filter_indicators(s, "l")),
        ("edit_mode", "key_other", "edit_mode", None),
        ("edit_mode", "key_s", "saving",
         lambda s: save_to_json_file(s, s['filename'])),
        ("selecting_o", "key_1", "action_menu", lambda s: show_menu(s, "o1")),
        ("selecting_o", "key_2", "action_menu", lambda s: show_menu(s, "o2")),
        ("selecting_o", "key_other", "selecting_o", None),
        ("selecting_l", "key_1", "action_menu", lambda s: show_menu(s, "l1")),
        ("selecting_l", "key_2", "action_menu", lambda s: show_menu(s, "l2")),
        ("selecting_l", "key_other", "selecting_l", None),
        ("action_menu", "menu_edit_text", "editing_text", edit_selected_text),
        ("action_menu", "menu_done", "edit_mode", None),
        ("editing_text", "text_edited", "edit_mode", redraw_diagram),
    ]


# --- Клавиатура ---
def key_press_event(state_data, event):
    """
    Обработчик нажатий клавиш. Определяет, какое событие произошло.
    Например: F — переход в режим редактирования.
    """
    key_text = event.text().lower()
    if event.key() == Qt.Key_F:
        state_data['event'] = "key_F"
    elif state_data['current_state'] == "edit_mode" and key_text == 'o':
        state_data['event'] = "key_o"
    elif state_data['current_state'] == "edit_mode" and key_text == 'l':
        state_data['event'] = "key_l"
    elif state_data['current_state'].startswith("selecting_") and key_text.isdigit():
        state_data['event'] = f"key_{key_text}"
    elif state_data['current_state'] == "edit_mode" and key_text == 's':
        state_data['event'] = "key_s"
    elif state_data['current_state'] == "edit_mode":
        state_data['event'] = "key_other"
    else:
        state_data['event'] = None
    process_event(state_data)


# --- Основная функция запуска диаграммы ---
def diagram_show(s_file_name, s_json):
    """
    Главная функция: создаёт приложение, сцену, окно и запускает главный цикл.
    """
    state_data = init_state_data()
    try:
        state_data['json_data'] = json.loads(s_json)
    except Exception as e:
        print(f"[Ошибка] Не удалось разобрать JSON: {e}")
        return False

    app = QApplication(sys.argv)
    scene = QGraphicsScene()
    view = QGraphicsView(scene)
    state_data['app'] = app
    state_data['scene'] = scene
    state_data['view'] = view

    def wrapped_key_event(event):
        key_press_event(state_data, event)

    scene.keyPressEvent = wrapped_key_event
    scene.drawForeground = lambda p, r: draw_foreground(state_data, p, r)

    scene_load_json(state_data)
    init_transition_table(state_data, s_file_name)

    view.setWindowTitle("DRAKON-SU — Минимальная схема")
    view.resize(500, 400)
    view.setRenderHint(QPainter.Antialiasing)
    view.setBackgroundBrush(Qt.lightGray)
    view.show()

    sys.exit(app.exec_())


# --- Точка входа ---
if __name__ == "__main__":
    """
    Пример начального JSON и запуск приложения.
    """
    example_json = '''
    {
        "items": {
            "item1": {"type": "start", "content": "Начало", "x": 100, "y": 50},
            "item2": {"type": "process", "content": "Вычисления"},
            "item3": {"type": "end", "content": "Конец"}
        }
    }
    '''
    diagram_show("example.json", example_json)
