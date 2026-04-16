# Скрипт обновляет значение

# import os
# import json

# def update_standard_in_json(file_path):
#     with open(file_path, 'r', encoding='utf-8') as f:
#         data = json.load(f)

#     updated = False
#     if "dimensions_details" in data:
#         for item in data["dimensions_details"]:
#             if "typeofproduct" in item:
#                 if not item["typeofproduct"]:  # если поле пустое
#                     item["typeofproduct"] = ""
#                     updated = True
#             else:
#                 item["typeofproduct"] = ""  # если поля нет вообще
#                 updated = True

#     if updated:
#         with open(file_path, 'w', encoding='utf-8') as f:
#             json.dump(data, f, ensure_ascii=False, indent=2)
#         print(f"Обновлён файл: {file_path}")

# def process_directory(directory):
#     for root, _, files in os.walk(directory):
#         for file in files:
#             if file.endswith('.json'):
#                 file_path = os.path.join(root, file)
#                 update_standard_in_json(file_path)

# if __name__ == "__main__":
#     target_dir = r"C:\Users\UTFC\Documents\БалтМебель\to\products"
#     process_directory(target_dir)
#     print("Обработка завершена.")



# Скрипт удаляет поле

import os
import json

def update_standard_in_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    updated = False
    if "dimensions_details" in data:
        for item in data["dimensions_details"]:
            if "skeleton" in item:
                del item["skeleton"]
                updated = True

    if updated:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Обновлён файл: {file_path}")

def process_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                update_standard_in_json(file_path)

if __name__ == "__main__":
    target_dir = r"C:\Users\UTFC\Documents\БалтМебель\to\products"
    process_directory(target_dir)
    print("Обработка завершена.")