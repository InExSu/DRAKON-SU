#!/bin/bash

# Проверка стиля кода
flake8 drakon_SU.py

# Оптимизированная сборка приложения
pyinstaller --clean --noconfirm --log-level=ERROR \
    --windowed --onedir \
    --name "DRAKON_SU" \
    --exclude-module PyQt5.QtWinExtras \
    --exclude-module PyQt5.QtWindowsExtras \
    drakon_SU.py

# Запуск приложения
/Users/michaelpopov/Documents/GitHub/DRAKON-SU/dist/DRAKON_SU.app/Contents/MacOS/DRAKON_SU
