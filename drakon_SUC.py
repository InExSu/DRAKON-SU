from PyQt5.QtWidgets import (QApplication, QGraphicsView, QGraphicsScene, 
                           QMainWindow)
from PyQt5.QtCore import QRectF
import sys
if sys.platform == 'win32':
    # Windows-specific adjustments
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)  # Для правильного масштабирования

def create_process(x, y, width, height, text, scene):
    """Создает прямоугольник процесса"""
    rect = scene.addRect(QRectF(x, y, width, height))
    text_item = scene.addText(text)
    text_item.setPos(x + 10, y + 10)
    return rect

def create_condition(x, y, size, text, scene):
    """Создает ромб условия"""
    pass

def main():
    """Основная функция приложения"""
    app = QApplication([])
    
    # Создаем главное окно
    window = QMainWindow()
    window.setWindowTitle("DRAKON SUC")
    window.resize(800, 600)
    
    # Создаем графическую сцену
    scene = QGraphicsScene()
    view = QGraphicsView(scene)
    window.setCentralWidget(view)
    
    # Добавляем тестовый элемент DRAKON
    create_process(50, 50, 200, 100, "Пример процесса", scene)
    
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()