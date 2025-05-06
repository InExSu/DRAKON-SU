from PyQt5.QtWidgets import (QApplication, QGraphicsView, QGraphicsScene,
                             QMainWindow)
from PyQt5.QtCore import QRectF
import sys
if sys.platform == 'win32':
    # Windows-specific adjustments
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)  # Для правильного масштабирования

import methods


def main():
    """Основная функция приложения"""
    app = QApplication([])

    # Создаем главное окно через отдельную функцию
    window, scene = create_main_window()

    window.show()

    s_User_Choice = methods.file_Choice([])

    # Бесконечный цикл обработки событий приложения
    app.exec_()


if __name__ == "__main__":
    main()
