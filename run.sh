#!/bin/bash


# Проверка стиля кода
# if ! flake8 drakon_SUC.py; then
#     echo "Исправьте ошибки стиля перед сборкой!"
#     exit 1
# fi

flake8 drakon_SUC.py

# Собрать приложение 
# python3 setup.py py2app
# python3 setup.py py2app --debug
pyinstaller --windowed --onedir --name "DRAKON_SUC" \
    --exclude-module PyQt5.QtWinExtras \
    --exclude-module PyQt5.QtWindowsExtras \
    --noconfirm \
    drakon_SUC.py

# запустить через терминал для получения подробного лога ошибок:
/Users/michaelpopov/Documents/GitHub/DRAKON-SUC/dist/DRAKON_SUC.app/Contents/MacOS/DRAKON_SUC
