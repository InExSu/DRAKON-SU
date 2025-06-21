import sys
import json

from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QWidget, QGraphicsTextItem, QMessageBox
from PyQt5.QtGui import QPainter, QPen, QBrush, QFont
from PyQt5.QtCore import Qt, QRectF


class DrakonItem:
    def __init__(self, item_id, item_type, content, x=100, y=50):
        self.id = item_id
        self.type = item_type
        self.content = content
        self.x = x
        self.y = y
        self.width = 120
        self.height = 60
        self.radius = 20

    def draw(self, painter):
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


class DrakonScene(QGraphicsScene):
    def __init__(self, json_data, parent=None):
        super().__init__(parent)
        self.json_data = json_data
        self.items_list = []
        self.lines = []
        self.indicators = []  # Список индикаторов
        self.edit_mode = False
        self.filter_prefix = ""

        self.parse_json()

    def parse_json(self):
        items_data = self.json_data.get("items", {})
        y = 50
        for item_id, data in items_data.items():
            item_type = data.get("type")
            content = data.get("content", "")
            x = data.get("x", 100)
            y = data.get("y", y)
            self.items_list.append(DrakonItem(item_id, item_type, content, x, y))
            y += 100  # Вертикальное расположение

        # Генерируем связи между элементами
        self.lines = []
        for i in range(len(self.items_list) - 1):
            self.lines.append({
                'start': self.items_list[i],
                'end': self.items_list[i + 1]
            })

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F:
            self.toggle_edit_mode()
        elif self.edit_mode:
            key_text = event.text().lower()
            if key_text == 'l':
                self.filter_prefix = 'l'
                self.update_indicators()
            elif key_text == 'o':
                self.filter_prefix = 'o'
                self.update_indicators()
            elif key_text.isdigit():
                selected_id = f"{self.filter_prefix}{key_text}"
                matches = [i for i in self.indicators if i.toPlainText() == selected_id]
                if len(matches) == 1:
                    self.show_menu(selected_id)

    def toggle_edit_mode(self):
        self.edit_mode = not self.edit_mode
        self.filter_prefix = ""
        self.clear_indicators()
        if self.edit_mode:
            self.add_indicators()

    def add_indicators(self):
        font = QFont("Arial", 10)
        # Индикаторы овалов (o1, o2...)
        for idx, item in enumerate(self.items_list):
            indicator = QGraphicsTextItem(f'o{idx+1}')
            indicator.setFont(font)
            indicator.setDefaultTextColor(Qt.darkGreen)
            indicator.setPos(item.x + item.width + 5, item.y + item.height // 3)
            self.addItem(indicator)
            self.indicators.append(indicator)

        # Индикаторы линий (l1, l2...)
        for idx, line in enumerate(self.lines):
            start = line['start']
            end = line['end']
            tx = (start.x + start.width // 2 + end.x + end.width // 2) // 2
            ty = (start.y + start.height + end.y) // 2
            indicator = QGraphicsTextItem(f'l{idx+1}')
            indicator.setFont(font)
            indicator.setDefaultTextColor(Qt.darkRed)
            indicator.setPos(tx, ty)
            self.addItem(indicator)
            self.indicators.append(indicator)

    def clear_indicators(self):
        for ind in self.indicators:
            self.removeItem(ind)
        self.indicators.clear()

    def update_indicators(self):
        self.clear_indicators()
        font = QFont("Arial", 10)

        # Отрисовка овалов
        for idx, item in enumerate(self.items_list):
            indicator_id = f"o{idx+1}"
            if self.filter_prefix == "" or indicator_id.startswith(self.filter_prefix):
                indicator = QGraphicsTextItem(indicator_id)
                indicator.setFont(font)
                indicator.setDefaultTextColor(Qt.darkGreen)
                indicator.setPos(item.x + item.width + 5, item.y + item.height // 3)
                self.addItem(indicator)
                self.indicators.append(indicator)

        # Отрисовка линий
        for idx, line in enumerate(self.lines):
            indicator_id = f"l{idx+1}"
            if self.filter_prefix == "" or indicator_id.startswith(self.filter_prefix):
                start = line['start']
                end = line['end']
                tx = (start.x + start.width // 2 + end.x + end.width // 2) // 2
                ty = (start.y + start.height + end.y) // 2
                indicator = QGraphicsTextItem(indicator_id)
                indicator.setFont(font)
                indicator.setDefaultTextColor(Qt.darkRed)
                indicator.setPos(tx, ty)
                self.addItem(indicator)
                self.indicators.append(indicator)

    def show_menu(self, selected_id):
        menu = QMessageBox()
        menu.setWindowTitle("Действие")
        menu.setText(f"Выбран {selected_id}")
        menu.addButton("Редактировать текст", QMessageBox.YesRole)
        menu.addButton("Формат", QMessageBox.NoRole)
        menu.exec_()

    def drawForeground(self, painter, rect):
        # Рисуем связи между элементами
        pen = QPen(Qt.black, 2)
        painter.setPen(pen)

        for line in self.lines:
            a = line['start']
            b = line['end']
            painter.drawLine(
                a.x + a.width // 2,
                a.y + a.height,
                b.x + b.width // 2,
                b.y
            )

        # Рисуем элементы диаграммы
        for item in self.items_list:
            item.draw(painter)

        # Если в режиме редактирования, ничего больше не делаем
        if self.edit_mode:
            return


class DrakonView(QGraphicsView):
    def __init__(self, scene, parent=None):
        super().__init__(scene, parent)
        self.setScene(scene)
        self.setWindowTitle("DRAKON-SU — Минимальная схема")
        self.resize(500, 400)
        self.setRenderHint(QPainter.Antialiasing)
        self.setBackgroundBrush(Qt.lightGray)

    def keyPressEvent(self, event):
        self.scene().keyPressEvent(event)


def diagram_Show(json_str):
    try:
        data = json.loads(json_str)
    except Exception as e:
        print(f"[Ошибка] Не удалось разобрать JSON: {e}")
        return False

    app = QApplication(sys.argv)
    scene = DrakonScene(data)
    view = DrakonView(scene)

    view.show()
    sys.exit(app.exec_())


# Пример использования
json_data = '''{
    "type": "drakon",
    "items": {
        "1": {
            "type": "start",
            "content": "Начало"
        },
        "2": {
            "type": "end",
            "content": "Конец"
        }
    }
}'''

diagram_Show(json_data)