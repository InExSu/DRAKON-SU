from PyQt5.QtWidgets import (QApplication, QGraphicsView, QGraphicsScene, 
                           QMainWindow, QDialog, QVBoxLayout, QPushButton, 
                           QButtonGroup)
from PyQt5.QtCore import QRectF
import sys

def file_Choice(files_Opened):
    """Функция выбора файла или действия"""
    dialog = QDialog()
    dialog.setWindowTitle("Выберите действие")
    layout = QVBoxLayout()
    
    # Создаем группу кнопок для управления выбором
    button_group = QButtonGroup()
    
    # Кнопка "Файл создать"
    btn_create = QPushButton("Файл создать")
    button_group.addButton(btn_create, 1)  # ID 1
    layout.addWidget(btn_create)
    
    # Кнопка "Файл открыть"
    btn_open = QPushButton("Файл открыть")
    button_group.addButton(btn_open, 2)  # ID 2
    layout.addWidget(btn_open)
    
    # Кнопки для ранее открытых файлов
    for i, file in enumerate(files_Opened, start=3):
        btn_file = QPushButton(file)
        button_group.addButton(btn_file, i)  # ID начинаются с 3
        layout.addWidget(btn_file)
    
    # Кнопка "Выход"
    btn_exit = QPushButton("Выход")
    button_group.addButton(btn_exit, 0)  # ID 0
    layout.addWidget(btn_exit)
    
    # Настраиваем диалог
    dialog.setLayout(layout)
    result = None
    
    # Обработчик нажатия кнопок
    def button_clicked(id):
        nonlocal result
        if id == 1:
            result = "Файл создать"
        elif id == 2:
            result = "Файл открыть"
        elif id == 0:
            result = "Выход"
        else:  # ID >= 3 - это файлы из files_Opened
            result = files_Opened[id - 3]
        dialog.accept()
    
    button_group.buttonClicked[int].connect(button_clicked)
    
    dialog.exec_()
    return result
