#!/bin/bash

# # Находим все .ts файлы в текущем каталоге (без подкаталогов)
# for file in *.ts; do
#   # Проверяем, существует ли файл
#   if [ -e "$file" ]; then
#     echo "eslint $file"
#     # Запускаем eslint для каждого файла в фоновом режиме
#     npx eslint "$file" --no-warn-ignored &
#   else
#     echo "Файлов .ts в текущем каталоге не найдено."
#   fi
# done

# # Ожидаем завершения всех фоновых процессов
# wait
# echo "eslint завершил проверку *.ts"

# Создаём каталог для резервных копий, если он ещё не существует
backup_dir="drn_BackUps"
mkdir -p "$backup_dir"

# Проверяем наличие .drn файлов в текущем каталоге
if ! ls *.drn >/dev/null 2>&1; then
    echo "Файлов .drn в текущем каталоге не найдено."
    exit 0
fi

# Проходим по всем файлам .drn в текущем каталоге
for file in *.drn; do
    # Пропускаем, если это не обычный файл (например, каталог)
    [ -f "$file" ] || continue

    # Формируем путь к файлу в каталоге резервных копий
    backup_file="$backup_dir/$file"

    # Проверяем, существует ли файл в каталоге резервных копий
    if [ -e "$backup_file" ]; then
        # Файл существует в backup_dir, сравниваем даты модификации
        if [ "$file" -nt "$backup_file" ]; then
            # Файл в текущем каталоге новее
            # Получаем текущую дату и время в формате YYYY-MM-DD HH-MM
            current_date=$(date +"%Y-%m-%d %H-%M")
            
            # Формируем новое имя для старого файла в backup_dir
            # Удаляем расширение .drn, добавляем дату-время и снова .drn
            new_backup_name="$backup_dir/${file%.drn} $current_date.drn"
            
            # Переименовываем старый файл в backup_dir
            mv "$backup_file" "$new_backup_name" &  
            echo "Старый файл переименован в: $new_backup_name"
            
            # Копируем свежий файл в backup_dir
            cp "$file" "$backup_file" &
            echo "Создана новая резервная копия: $backup_file"
        else
            echo "Файл $file не обновлён, так как он не новее резервной копии"
        fi
    else
        # Файла нет в backup_dir, просто копируем
        cp "$file" "$backup_file" &
        echo "Создана новая резервная копия: $backup_file"
    fi
done

wait

# clasp push