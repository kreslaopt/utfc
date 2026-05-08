import os
import json

def clear_additional_in_images(data):
    if 'images' in data and isinstance(data['images'], list):
        for image_obj in data['images']:
            if 'additional' in image_obj and isinstance(image_obj['additional'], list):
                # Очистить массив additional
                image_obj['additional'] = []
    return data

def process_json_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    data = clear_additional_in_images(data)
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