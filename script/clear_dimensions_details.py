import os
import json

def clear_dimensions_details(data):
    if 'dimensions_details' in data and isinstance(data['dimensions_details'], list):
        for obj in data['dimensions_details']:
            # Очистить массив additional, если он есть
           
                obj.clear()
    return data

def process_json_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    data = clear_dimensions_details(data)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def process_folder(folder_path):
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.json'):
                filepath = os.path.join(root, file)
                try:
                    process_json_file(filepath)
                    print(f"Обработан: {filepath}")
                except Exception as e:
                    print(f"Ошибка при обработке {filepath}: {e}")

folder_path = r"C:\Users\UTFC\Documents\БалтМебель\to\products"
process_folder(folder_path)