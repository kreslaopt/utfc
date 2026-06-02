import json
import re

file_path = r"C:\Users\UTFC\Documents\БалтМебель\to\script\merged_result.json"
log_file_path = r"C:\Users\UTFC\Documents\БалтМебель\to\script\debug_log.txt"

log_file = open(log_file_path, 'w', encoding='utf-8')

def log(message):
    print(message)
    log_file.write(message + '\n')

def count_links(ip_prop36_value):
    if not ip_prop36_value:
        return 0
    value = re.sub(r"&nbsp;|<[^>]+>", "", ip_prop36_value).strip()
    if not value:
        return 0
    log(f"Обрабатываемое значение: '{value}'")
    if "," in value:
        links = [link.strip() for link in value.split(",") if link.strip()]
    elif " " in value:
        links = [link.strip() for link in value.split() if link.strip()]
    else:
        links = [value]
    log(f"Найденные ссылки: {links}")
    return len(links)

def process_item(item, groups):
    ie_name = item.get("IE_NAME", "").strip()
    ip_prop36 = item.get("IP_PROP36")
    
    # Логируем каждый элемент для диагностики
    log(f"Обработка элемента: IE_NAME='{ie_name}', IP_PROP36='{ip_prop36}', тип IE_NAME={type(ie_name)}")
    log(f"Полный элемент: {json.dumps(item, ensure_ascii=False)}")
    
    # Обрабатываем только если есть IE_NAME
    if ie_name:
        # Обработка данных
        if isinstance(ip_prop36, list):
            count_links_in_item = len(ip_prop36)
        elif isinstance(ip_prop36, str):
            count_links_in_item = count_links(ip_prop36)
        else:
            count_links_in_item = 0
        
        # Сохраняем в группы
        if count_links_in_item in groups:
            groups[count_links_in_item].append(ie_name)
    else:
        log(f"Элемент пропущен, IE_NAME пустое или отсутствует")
    
    # Обработка вложенных элементов
    children = item.get("children", [])
    for child in children:
        process_item(child, groups)

with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

groups = {i: [] for i in range(6)}
processed_counter = 0

for item in data:
    process_item(item, groups)

log(f"\nОбработано элементов с IE_NAME: {sum(len(v) for v in groups.values())}")

for count in sorted(groups.keys(), reverse=True):
    log(f"\nЭлементы с {count} ссылками в IP_PROP36:")
    for ie_name in groups[count]:
        log(f" - {ie_name} ({count} ссылок)")

log_file.close()