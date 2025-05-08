# дать права на выполнение файлов
find . -name "*.sh" -exec chmod +x {} +
# возвраты кареток заменить
for file in *.sh; do dos2unix "$file"; done
# получить права на изменение файлов
sudo chown -R $(whoami):$(id -gn) .

# уменьшить размер гит
git gc --prune=now --aggressive

# Активация виртуального окружения
source venv/bin/activate
# Деактивация виртуального окружения
deactivate
# запуск проекта
python3 /Users/michaelpopov/Documents/GitHub/DRAKON-SUC/drakon_SUC.py
# или
./run.sh

# Собрать приложение 
# python3 setup.py py2app
# python3 setup.py py2app --debug
pyinstaller --windowed --onedir --name "DRAKON_SUC" drakon_SUC.py --noconfirm

# запустить через терминал для получения подробного лога ошибок:
/Users/michaelpopov/Documents/GitHub/DRAKON-SUC/dist/DRAKON_SUC.app/Contents/MacOS/DRAKON_SUC

# запускать приложение
# open /Users/michaelpopov/Documents/GitHub/DRAKON-SUC/dist/DRAKON_SUC.app
open dist/DRAKON_SUC.app