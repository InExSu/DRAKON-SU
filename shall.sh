find . -name "*.sh" -exec chmod +x {} +
for file in *.sh; do dos2unix "$file"; done
# получить права на изменение файлов
sudo chown -R $(whoami):$(id -gn) .

# запуск проекта
python3 /Users/michaelpopov/Documents/GitHub/DRAKON-SUC/drakon_SUC.py
# или
./run.sh

# Собрать приложение 
python3 setup.py py2app

# запустить через терминал для получения подробного лога ошибок:
/Users/michaelpopov/Documents/GitHub/DRAKON-SUC/dist/DRAKON\ Editor.app/Contents/MacOS/DRAKON\ Editor

# запускать приложение
open /Users/michaelpopov/Documents/GitHub/DRAKON-SUC/dist/DRAKON\ Editor.app
