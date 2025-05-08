#!/bin/bash

# Проверка стиля кода
flake8 drakon_SUC.py

# Оптимизированная сборка приложения
pyinstaller --clean --noconfirm --log-level=ERROR \
    --windowed --onedir \
    --name "DRAKON_SUC" \
    --exclude-module PyQt5.QtWinExtras \
    --exclude-module PyQt5.QtWindowsExtras \
    drakon_SUC.py

# Запуск приложения
/Users/michaelpopov/Documents/GitHub/DRAKON-SUC/dist/DRAKON_SUC.app/Contents/MacOS/DRAKON_SUC
