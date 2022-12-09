# ⚠️GRAPH-ATTACK⚠️
Данный скрипт предназначен для отрисовки графов атак.
Входящие данные состоят из 3 файлов:
1. Файл с топологией сети
   
   Пример:
   
   `IP-адрес узла сети : уязвимость, присутствующая на узле`
2. Файл связей
   
   Пример:
   
   ```
   IP-адрес маршрутизатора:
   > IP-адреса соединенных маршрутизаторов
   + IP-адрес узла, доступного для внешней сети
   - IP-адрес узла, недоступного для внешней сети
   ```
3. Файл с информацией об уязвимостях
   
   Пример:
   
   `Уязвимость : уровень предостовляемого доступа на узлах`

## Для начала работы:

```
python -m venv venv
pip install -r requirements.txt
```

Файлом для запуска программы является app.py

**Результаты** выполнения находятся в папке `/src/results`