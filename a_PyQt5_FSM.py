
# На память. Из этого кода сделал a_PyQt5_Imper.py без классов

import sys
import json

from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsTextItem, QMessageBox, QInputDialog
from PyQt5.QtGui import QPainter, QPen, QBrush, QFont
from PyQt5.QtCore import Qt, QRectF

def scene_SaveToJsonFile(self, filename="updated_diagram.json"):
    """Сохраняет текущее состояние диаграммы в файл"""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.json_Data, f, ensure_ascii=False, indent=4)
        print(f"[OK] Диаграмма сохранена в {filename}")
    except Exception as e:
        print(f"[Ошибка] Не удалось сохранить файл: {e}")

def diagram_Show(s_File_Name, s_JSON):
    """
    Отображает диаграмму на основе строки JSON.
    """
    try:
        data = json.loads(s_JSON)
    except Exception as e:
        print(f"[Ошибка] Не удалось разобрать JSON: {e}")
        return False

    # Инициализируем приложение Qt, передаём аргументы командной строки
    app = QApplication(sys.argv)

    # Создаём сцену диаграммы, используя JSON-данные и имя файла
    scene = DiagramScene(data, s_File_Name)

    # Создаём графическое представление (окно) и привязываем к нему сцену
    view = DiagramView(scene)

    # Отображаем главное окно приложения
    view.show()

    # Запускаем главный цикл обработки событий Qt
    sys.exit(app.exec_())
    
class DiagramElement:
    def __init__(self, item_id, item_type, content, x=100, y=50):
        self.id = item_id
        self.type = item_type
        self.content = content
        self.x = x
        self.y = y
        self.width = 120
        self.height = 60
        self.radius = 20

    def element_Draw(self, painter):
        """Рисует элемент диаграммы"""
        painter.save()
        if self.type == "start":
            brush = QBrush(Qt.blue)
            pen = QPen(Qt.white, 2)
            painter.setBrush(brush)
            painter.setPen(pen)
            painter.drawRoundedRect(self.x, self.y, self.width, self.height, self.radius, self.radius)
        elif self.type == "end":
            brush = QBrush(Qt.red)
            pen = QPen(Qt.white, 2)
            painter.setBrush(brush)
            painter.setPen(pen)
            painter.drawRoundedRect(self.x, self.y, self.width, self.height, self.radius, self.radius)
        else:
            brush = QBrush(Qt.lightGray)
            pen = QPen(Qt.black, 2)
            painter.setBrush(brush)
            painter.setPen(pen)
            painter.drawRect(self.x, self.y, self.width, self.height)

        painter.setPen(Qt.white if self.type in ["start", "end"] else Qt.black)
        painter.setFont(QFont("Arial", 10))
        text_rect = QRectF(self.x, self.y, self.width, self.height)
        painter.drawText(text_rect, Qt.AlignCenter, self.content)
        painter.restore()


class DiagramScene(QGraphicsScene):
    def __init__(self, json_data, s_File_Name, parent=None):
        super().__init__(parent)
        self.json_Data = json_data
        self.element_List = []
        self.link_List = []
        self.indicator_List = []

        # FSM
        self.state = "idle"
        self.event = None
        self.selected_Indicator = None
        self.selected_Element = None
        self.filter_Prefix = ""

        # Загружаем данные
        self.scene_LoadJson()

        # Таблица переходов (технология Шалыто)
        self.transition_Table = [
            # state       event           new_state     action
            ("idle",      "key_F",       "edit_mode",      self.scene_AddIndicators),
            ("edit_mode", "key_o",       "selecting_o",    self.scene_FilterIndicatorsO),
            ("edit_mode", "key_l",       "selecting_l",    self.scene_FilterIndicatorsL),
            ("edit_mode", "key_other",   "edit_mode",      None),
            ("edit_mode", "key_s", "saving", scene_SaveToJsonFile(s_File_Name)),

            ("selecting_o", "key_1",    "action_menu",    lambda: self.scene_ShowMenu("o1")),
            ("selecting_o", "key_2",    "action_menu",    lambda: self.scene_ShowMenu("o2")),
            ("selecting_o", "key_other","selecting_o",    None),
            
            ("selecting_l", "key_1",    "action_menu",    lambda: self.scene_ShowMenu("l1")),
            ("selecting_l", "key_2",    "action_menu",    lambda: self.scene_ShowMenu("l2")),
            ("selecting_l", "key_other","selecting_l",    None),

            ("action_menu", "menu_edit_text", "editing_text", self.scene_EditSelectedText),
            ("action_menu", "menu_done",    "edit_mode",    None),
            ("editing_text", "text_edited", "edit_mode",   self.scene_RedrawDiagram),
        ]

    def keyPressEvent(self, event):
        """Обработка событий клавиатуры"""
        key_text = event.text().lower()
        if event.key() == Qt.Key_F:
            self.event = "key_F"
        elif self.state == "edit_mode" and key_text == 'o':
            self.event = "key_o"
        elif self.state == "edit_mode" and key_text == 'l':
            self.event = "key_l"
        elif self.state.startswith("selecting_") and key_text.isdigit():
            self.event = f"key_{key_text}"
        elif self.state == "edit_mode":
            self.event = "key_other"
        elif self.state == "action_menu":
            pass  # Ждём действия через меню
        elif self.state == "edit_mode" and key_text == 's':
            self.event = "key_s"
        else:
            self.event = None

        self.scene_ProcessEvent()

    def scene_ProcessEvent(self):
        """Обрабатывает событие согласно таблице переходов"""
        for row in self.transition_Table:
            current_state, current_event, new_state, action = row
            if self.state == current_state and self.event == current_event:
                self.state = new_state
                if action:
                    action()
                self.event = None
                return

        print(f"[!] Неизвестный переход: {self.state} + {self.event}")

    def scene_LoadJson(self):
        """Загружает JSON и создаёт элементы диаграммы"""
        items_data = self.json_Data.get("items", {})
        y = 50
        for item_id, data in items_data.items():
            item_type = data.get("type")
            content = data.get("content", "")
            x = data.get("x", 100)
            y = data.get("y", y)
            self.element_List.append(DiagramElement(item_id, item_type, content, x, y))
            y += 100

        # Создаём связи между элементами
        self.link_List = []
        for i in range(len(self.element_List) - 1):
            self.link_List.append({
                'start': self.element_List[i],
                'end': self.element_List[i + 1]
            })

    def scene_AddIndicators(self):
        """Добавляет все индикаторы ('o1', 'l1')"""
        font = QFont("Arial", 10)
        self.scene_ClearIndicators()

        for idx, item in enumerate(self.element_List):
            indicator = QGraphicsTextItem(f"o{idx+1}")
            indicator.setFont(font)
            indicator.setDefaultTextColor(Qt.darkGreen)
            indicator.setPos(item.x + item.width + 5, item.y + item.height // 3)
            self.addItem(indicator)
            self.indicator_List.append(indicator)

        for idx, link in enumerate(self.link_List):
            start = link['start']
            end = link['end']
            tx = (start.x + start.width // 2 + end.x + end.width // 2) // 2
            ty = (start.y + start.height + end.y) // 2
            indicator = QGraphicsTextItem(f"l{idx+1}")
            indicator.setFont(font)
            indicator.setDefaultTextColor(Qt.darkRed)
            indicator.setPos(tx, ty)
            self.addItem(indicator)
            self.indicator_List.append(indicator)

    def scene_FilterIndicatorsO(self):
        self.scene_FilterIndicators("o")

    def scene_FilterIndicatorsL(self):
        self.scene_FilterIndicators("l")

    def scene_FilterIndicators(self, prefix):
        self.scene_ClearIndicators()
        font = QFont("Arial", 10)

        for idx, item in enumerate(self.element_List):
            indicator_id = f"o{idx+1}"
            if indicator_id.startswith(prefix):
                indicator = QGraphicsTextItem(indicator_id)
                indicator.setFont(font)
                indicator.setDefaultTextColor(Qt.darkGreen)
                indicator.setPos(item.x + item.width + 5, item.y + item.height // 3)
                self.addItem(indicator)
                self.indicator_List.append(indicator)

        for idx, link in enumerate(self.link_List):
            indicator_id = f"l{idx+1}"
            if indicator_id.startswith(prefix):
                start = link['start']
                end = link['end']
                tx = (start.x + start.width // 2 + end.x + end.width // 2) // 2
                ty = (start.y + start.height + end.y) // 2
                indicator = QGraphicsTextItem(indicator_id)
                indicator.setFont(font)
                indicator.setDefaultTextColor(Qt.darkRed)
                indicator.setPos(tx, ty)
                self.addItem(indicator)
                self.indicator_List.append(indicator)

    def scene_ShowMenu(self, selected_id):
        """Показывает контекстное меню"""
        menu = QMessageBox()
        menu.setWindowTitle("Действие")
        menu.setText(f"Выбран {selected_id}")
        btn_edit = menu.addButton("Редактировать текст", QMessageBox.YesRole)
        btn_format = menu.addButton("Формат", QMessageBox.NoRole)
        btn_cancel = menu.addButton("Отмена", QMessageBox.RejectRole)

        result = menu.exec_()
        clicked_button = menu.clickedButton()

        if clicked_button == btn_edit:
            self.selected_Indicator = selected_id
            self.state = "action_menu"
            self.event = "menu_edit_text"
            self.scene_ProcessEvent()
        elif clicked_button == btn_format:
            print("Форматирование не реализовано — можно добавить позже")
        else:
            self.state = "edit_mode"

    def scene_EditSelectedText(self):
        """Вызывает диалог редактирования текста"""
        if not self.selected_Indicator:
            return

        # Извлекаем номер из индикатора
        indicator_number = int(self.selected_Indicator[1:]) - 1

        if self.selected_Indicator.startswith("o"):
            target_element = self.element_List[indicator_number]
        elif self.selected_Indicator.startswith("l"):
            target_element = self.link_List[indicator_number]['start']
        else:
            return

        # Сохраняем ссылку на элемент для последующего редактирования
        self.selected_Element = target_element

        # Вызываем диалог
        new_text, ok = QInputDialog.getText(None, "Редактировать текст", "Введите новый текст:", text=target_element.content)
        if ok and new_text:
            target_element.content = new_text
            self.event = "text_edited"
            self.scene_ProcessEvent()
        else:
            self.state = "edit_mode"

    def scene_RedrawDiagram(self):
        """Перерисовывает диаграмму после редактирования"""
        self.update()  # Это вызовет drawForeground автоматически

    def scene_ClearIndicators(self):
        """Удаляет индикаторы с экрана"""
        for ind in self.indicator_List:
            self.removeItem(ind)
        self.indicator_List.clear()

    def drawForeground(self, painter, rect):
        """Основная отрисовка связей и элементов"""
        # Рисуем связи
        pen = QPen(Qt.black, 2)
        painter.setPen(pen)
        for link in self.link_List:
            a = link['start']
            b = link['end']
            painter.drawLine(
                a.x + a.width // 2,
                a.y + a.height,
                b.x + b.width // 2,
                b.y
            )

        # Рисуем элементы
        for element in self.element_List:
            element.element_Draw(painter)


class DiagramView(QGraphicsView):
    def __init__(self, scene, parent=None):
        super().__init__(scene, parent)
        self.setScene(scene)
        self.setWindowTitle("DRAKON-SU — Минимальная схема")
        self.resize(500, 400)
        self.setRenderHint(QPainter.Antialiasing)
        self.setBackgroundBrush(Qt.lightGray)

    def keyPressEvent(self, event):
        """Передаём нажатие клавиш в сцену"""
        self.scene().keyPressEvent(event)


# def diagram_Run(json_str):
#     try:
#         data = json.loads(json_str)
#     except Exception as e:
#         print(f"[Ошибка] Не удалось разобрать JSON: {e}")
#         return False

#     app = QApplication(sys.argv)
#     scene = DiagramScene(data)
#     view = DiagramView(scene)

#     view.show()
#     sys.exit(app.exec_())


# # Пример JSON
# json_Data = '''{
#     "type": "drakon",
#     "items": {
#         "1": {
#             "type": "start",
#             "content": "Начало"
#         },
#         "2": {
#             "type": "end",
#             "content": "Конец"
#         }
#     }
# }'''

# diagram_Run(json_Data)