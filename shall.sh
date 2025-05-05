find . -name "*.sh" -exec chmod +x {} +
for file in *.sh; do dos2unix "$file"; done
# получить права на изменение файлов
sudo chown -R $(whoami):$(id -gn) .

# запуск проекта
python3 /Users/michaelpopov/Documents/GitHub/DRAKON-SUC/drakon_SUC.py
# или
./run.sh