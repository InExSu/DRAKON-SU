import sys
import json

from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QWidget
from PyQt5.QtGui import QPainter, QPen, QBrush, QFont, QPainterPath
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

        # Текст
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
            y += 100  # Смещаем следующий элемент ниже

    def drawForeground(self, painter, rect):
        # Рисуем связи между элементами
        pen = QPen(Qt.black, 2)
        painter.setPen(pen)

        for i in range(len(self.items_list) - 1):
            a = self.items_list[i]
            b = self.items_list[i + 1]
            painter.drawLine(
                a.x + a.width // 2,
                a.y + a.height,
                b.x + b.width // 2,
                b.y
            )

        # Рисуем элементы поверх связей
        for item in self.items_list:
            item.draw(painter)


class DrakonView(QGraphicsView):
    def __init__(self, scene, parent=None):
        super().__init__(scene, parent)
        self.setScene(scene)
        self.setWindowTitle("DRAKON-SU — Минимальная схема")
        self.resize(400, 300)
        self.setRenderHint(QPainter.Antialiasing)
        self.setBackgroundBrush(Qt.lightGray)


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