Формат без явного указания позиций - визуализатор автоматически размещает элементы:

```yaml
header: |
  import math
  import io
  MAX_BUFFER = 1024

---
functions:
  read_file:
    description: "Чтение файла с проверкой существования"
    parameters: ["path: str"]
    returns: "str"
    nodes:
      - id: 1
        type: "start"
        text: "Начало"
        connections: [2]
      
      - id: 2
        type: "condition"
        text: "Файл существует?"
        connections: {yes: 3, no: 6}
      
      - id: 3
        type: "collapsible"
        text: "Чтение файла"
        default_state: "collapsed"
        connections: [7]
        contains:
          - id: 3.1
            type: "action"
            text: "file = open(path, 'r')"
            connections: [3.2]
            
          - id: 3.2
            type: "action"
            text: "content = file.read()"
            connections: [3.3]
            
          - id: 3.3
            type: "action"
            text: "file.close()"
            connections: []
      
      - id: 6
        type: "action"
        text: "raise FileNotFoundError"
        connections: [8]
      
      - id: 7
        type: "action" 
        text: "return content"
        connections: [8]
      
      - id: 8
        type: "end"
        text: "Конец"
        connections: []

  process_content:
    description: "Обработка содержимого файла"
    parameters: ["content: str"]
    returns: "list"
    nodes:
      - id: 1
        type: "start"
        text: "Начало"
        connections: [2]
      
      - id: 2
        type: "action"
        text: "lines = content.split('\\n')"
        connections: [3]
      
      - id: 3
        type: "action"
        text: "return [line for line in lines if line.strip()]"
        connections: [4]
      
      - id: 4
        type: "end"
        text: "Конец"
        connections: []

---
footer: |
  if __name__ == "__main__":
      try:
          data = read_file("input.txt")
          result = process_content(data)
          print(f"Прочитано {len(result)} строк")
      except FileNotFoundError:
          print("Файл не найден!")
```

### Ключевые изменения:
1. **Удалены все `position`** - визуализатор будет автоматически рассчитывать расположение элементов
2. **Сохранена полная структура**:
   - Метаданные
   - Header/Footer с многострочным кодом
   - Функции с узлами разных типов
3. **Поддержка сворачиваемых блоков**:
   - Параметр `default_state` ("collapsed"/"expanded")
   - Вложенные узлы в секции `contains`
4. **Четкие связи** через `connections`

### Преимущества формата:
- Автоматическая компоновка схемы
- Читаемость за счет YAML-синтаксиса
- Поддержка сложных структур (ветвления, циклы, сворачиваемые блоки)
- Легко расширяется новыми типами узлов

Визуализатор сможет использовать алгоритм автоматического размещения, учитывая:
1. Иерархию узлов
2. Типы соединений
3. Вложенность блоков
4. Оптимальное использование пространства

### **Пример схемы с параллельным выполнением (fork-join модель) в DRAKON-формате**

Формат использует специальные узлы `fork` (разделение потока) и `join` (синхронизация), а также сохраняет автоматическое позиционирование.

```yaml
---
header:
---
functions:
  process_data:
    description: "Параллельная обработка данных"
    parameters: ["data: list"]
    returns: "dict"
    nodes:
      # Старт
      - id: start
        type: "start"
        connections: ["fork_split"]

      # Разделение на 3 потока
      - id: fork_split
        type: "fork"
        text: "Параллельная обработка"
        connections: ["preprocess", "validate", "analyze"]  # 3 параллельных ветки

      # --- Ветка 1: Предобработка ---
      - id: preprocess
        type: "action"
        text: "temp1 = preprocess_data(data)"
        connections: ["join_node"]

      # --- Ветка 2: Валидация ---
      - id: validate
        type: "action"
        text: "temp2 = validate_data(data)"
        connections: ["join_node"]

      # --- Ветка 3: Анализ ---
      - id: analyze
        type: "collapsible"
        text: "Анализ данных"
        default_state: "expanded"
        connections: ["join_node"]
        contains:
          - id: analyze_step1
            type: "action"
            text: "stats = calculate_stats(data)"
            connections: ["analyze_step2"]
          - id: analyze_step2
            type: "action"
            text: "temp3 = normalize(stats)"

      # Синхронизация
      - id: join_node
        type: "join"
        text: "Ожидание завершения"
        connections: ["merge_results"]

      # Объединение результатов
      - id: merge_results
        type: "action"
        text: "return {'pre': temp1, 'valid': temp2, 'stats': temp3}"
        connections: ["end"]

      # Завершение
      - id: end
        type: "end"
---
footer: |
  # Пример использования
  if __name__ == "__main__":
      data = load_dataset()
      result = process_data(data)
      print(result)
```

### **Особенности реализации:**
1. **Узлы `fork` и `join`:**
   - `fork` создает параллельные ветки (аналог `Promise.all` в JS или `multiprocessing` в Python)
   - `join` ожидает завершения всех веток

2. **Визуализация:**
```mermaid
flowchart TD
    Start([Start]) --> Fork{Fork}
    Fork --> B1[Ветка 1: Предобработка]
    Fork --> B2[Ветка 2: Валидация]
    Fork --> B3[Ветка 3: Анализ]
    
    B1 --> Join((Join))
    B2 --> Join
    B3 --> Join
    
    Join --> Merge[Объединение результатов]
    Merge --> End([End])
   ```

3. **Семантика выполнения:**
   - Все ветки между `fork` и `join` выполняются конкурентно
   - Ветки могут содержать:
     - Простые действия (`action`)
     - Сворачиваемые блоки (`collapsible`)
     - Другие управляющие конструкции

4. **Генерация кода** (пример на Python):
   ```python
   def process_data(data):
       with ThreadPoolExecutor() as executor:
           # Запуск параллельных задач
           future1 = executor.submit(preprocess_data, data)
           future2 = executor.submit(validate_data, data)
           future3 = executor.submit(calculate_stats, data)
       
       # Ожидание результатов (автоматически в join)
       temp1 = future1.result()
       temp2 = future2.result()
       temp3 = future3.result()
       
       return {'pre': temp1, 'valid': temp2, 'stats': temp3}
   ```

### **Поддерживаемые варианты параллелизма:**
- Потоки (threads)
- Процессы (multiprocessing)
- Асинхронные задачи (async/await)
- Распределенные вычисления (через очереди задач)

Формат остается агностичным к реализации, оставляя выбор механизма за кодогенератором.

====
Код файла для визуализатора:

Вот полный пример файла в формате `.drakon`, включающий все запрошенные элементы:

```yaml

header: |
  # Импорты и константы
  import numpy as np
  from typing import Union
  MAX_ATTEMPTS = 3

---
functions:
  # Простая функция (линейный алгоритм)
  calculate_sum:
    description: "Суммирует элементы массива"
    parameters: ["arr: list[float]"]
    returns: "float"
    nodes:
      - id: start
        type: "start"
        connections: ["init"]
      
      - id: init
        type: "action"
        text: "total = 0.0"
        connections: ["loop_start"]
      
      - id: loop_start
        type: "silhouette_start"
        text: "Цикл суммирования"
        connections: ["loop_cond"]
      
      - id: loop_cond
        type: "condition"
        text: "i < len(arr)?"
        connections: {yes: "loop_body", no: "silhouette_end"}
      
      - id: loop_body
        type: "action"
        text: "total += arr[i]"
        connections: ["loop_inc"]
      
      - id: loop_inc
        type: "action"
        text: "i += 1"
        connections: ["loop_cond"]
      
      - id: silhouette_end
        type: "silhouette_end"
        connections: ["result"]
      
      - id: result
        type: "action"
        text: "return total"
        connections: ["end"]
      
      - id: end
        type: "end"

  # Сложная функция (все элементы)
  data_processor:
    description: "Обработка данных со всеми конструкциями"
    parameters: ["data: Union[list, dict]", "mode: int"]
    returns: "dict"
    nodes:
      # Стартовая секция
      - id: start
        type: "start"
        connections: ["input_check"]
      
      # Ветвление if-else
      - id: input_check
        type: "condition"
        text: "isinstance(data, dict)?"
        connections: {yes: "dict_process", no: "list_process"}
      
      # Обработка словаря (свертываемый блок)
      - id: dict_process
        type: "collapsible"
        text: "Обработка словаря"
        default_state: "collapsed"
        connections: ["merge_point"]
        contains:
          - id: dp1
            type: "action"
            text: "keys = list(data.keys())"
            connections: ["dp2"]
          - id: dp2
            type: "action"
            text: "values = [float(x) for x in data.values()]"
            connections: ["dp3"]
          - id: dp3
            type: "action"
            text: "processed = dict(zip(keys, values))"
      
      # Обработка списка (параллельные задачи)
      - id: list_process
        type: "fork"
        text: "Параллельная обработка"
        connections: ["stats_calc", "clean_data", "validate"]
      
      # Параллельные ветки
      - id: stats_calc
        type: "action"
        text: "mean = np.mean(data)"
        connections: ["join_point"]
      
      - id: clean_data
        type: "action"
        text: "cleaned = [x for x in data if not np.isnan(x)]"
        connections: ["join_point"]
      
      - id: validate
        type: "condition"
        text: "len(data) > 0?"
        connections: {yes: "join_point", no: "error_handler"}
      
      # Точка синхронизации
      - id: join_point
        type: "join"
        text: "Объединение результатов"
        connections: ["merge_point"]
      
      # Переход (аналог goto)
      - id: error_handler
        type: "action"
        text: "log_error('Empty input')"
        connections: ["merge_point"]
      
      # Точка слияния
      - id: merge_point
        type: "action"
        text: "merged = locals()"
        connections: ["mode_switch"]
      
      # Switch-case конструкция
      - id: mode_switch
        type: "condition"
        text: "mode"
        connections: {
          "1": "format_json",
          "2": "format_xml",
          "default": "format_csv"
        }
      
      # Варианты обработки
      - id: format_json
        type: "action"
        text: "result = json.dumps(merged)"
        connections: ["finalize"]
      
      - id: format_xml
        type: "action"
        text: "result = dicttoxml(merged)"
        connections: ["finalize"]
      
      - id: format_csv
        type: "action"
        text: "result = pd.DataFrame(merged).to_csv()"
        connections: ["finalize"]
      
      # Финализация
      - id: finalize
        type: "silhouette_start"
        text: "Финальные операции"
        connections: ["save_log"]
      
      - id: save_log
        type: "action"
        text: "write_log(result)"
        connections: ["silhouette_end"]
      
      - id: silhouette_end
        type: "silhouette_end"
        connections: ["return_result"]
      
      - id: return_result
        type: "action"
        text: "return {'data': result, 'status': 'OK'}"
        connections: ["end"]
      
      - id: end
        type: "end"

---
footer: |
  # Пример использования
  if __name__ == "__main__":
      test_data = [1.2, 3.4, 5.6]
      print(calculate_sum(test_data))
      
      result = data_processor(
          data={"temp": 42, "pressure": 1013},
          mode=2
      )
      print(result)
```

### Ключевые элементы в файле:
1. **Простая функция** (`calculate_sum`):
   - Линейный алгоритм
   - Использование силуэта для цикла
   - Четкая последовательность действий

2. **Сложная функция** (`data_processor`):
   - Ветвление (if-else)
   - Switch-case конструкция через condition с multiple outputs
   - Параллельное выполнение (fork-join)
   - Свертываемый блок для сложной логики
   - Силуэты для группировки
   - Аналог GOTO через явные соединения
   - Обработка ошибок

3. **Форматирование**:
   - Четкая структура YAML
   - Подробные описания
   - Соответствие стандартам DRAKON

4. **Полноценный пример**:
   - Метаданные
   - Header с импортами
   - Две функции разной сложности
   - Footer с примером использования

Файл готов для обработки визуализатором и содержит все запрошенные элементы.