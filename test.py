from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QGraphicsTextItem, QGraphicsLineItem
from PyQt5.QtCore import Qt, QRectF, QLineF
import sys

class DiagramWindow(QMainWindow):
    def __init__(self):
        """Инициализация главного окна"""
        super().__init__()
        self.setWindowTitle("DRAKON Diagram")
        self.setGeometry(100, 100, 400, 300)
        
        # Создаем сцену и вид
        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene, self)
        self.setCentralWidget(self.view)
        
        # Рисуем элементы диаграммы
        self.draw_diagram()

    def draw_diagram(self):
        """Метод для рисования диаграммы"""
        # Первый прямоугольник с текстом
        rect1 = QGraphicsRectItem(QRectF(50, 50, 100, 50))
        rect1.setBrush(Qt.white)
        self.scene.addItem(rect1)
        
        text1 = QGraphicsTextItem("01")
        text1.setPos(85, 65)
        self.scene.addItem(text1)
        
        # Второй прямоугольник с текстом
        rect2 = QGraphicsRectItem(QRectF(50, 150, 100, 50))
        rect2.setBrush(Qt.white)
        self.scene.addItem(rect2)
        
        text2 = QGraphicsTextItem("02")
        text2.setPos(85, 165)
        self.scene.addItem(text2)
        
        # Линия между прямоугольниками
        line = QGraphicsLineItem(QLineF(100, 100, 100, 150))
        self.scene.addItem(line)

def main():
    """Основная функция приложения"""
    app = QApplication(sys.argv)
    window = DiagramWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()