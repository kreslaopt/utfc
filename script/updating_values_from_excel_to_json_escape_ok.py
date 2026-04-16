import pandas as pd
import json
import os
import re
import math

parents_mapping = {
    # 'модель_дочерняя': 'модель_родитель',
    'кора ch': 'кора черный',
    'Кора чёрный': 'кора черный',
    'изо': 'изо сн',
}


# Функция нормализации имени модели
def normalize_model_name(name):
    if not isinstance(name, str):
        return ""
    name = name.lower().strip()
    name = re.sub(r'\bстул\b|\bкресло\b|Кресло UTFC\b', '', name, flags=re.IGNORECASE)
    name = re.sub(r'сн\s*-?\s*710\s+айкью', 'айкью', name, flags=re.IGNORECASE)
    name = re.sub(r'сн\s*-?\s*800\s+энжел', 'энжел', name, flags=re.IGNORECASE)
    name = re.sub(r'н\/п|н_п', 'нп', name)
    name = re.sub(r'[/\\]', ' ', name)
    name = re.sub(r'\s+', ' ', name)
    name = re.sub(r'[^\w\s+-]', '', name)
    name = re.sub(r'пластик\/хром|пластик хром', 'пластикхром', name)
    name = re.sub(r'хром\/хдп\/мб|хром хдп мб', 'хромхдпмб', name)
    name = re.sub(r'дерево\/мб|дерево мб', 'деревомб', name)
    name = re.sub(r'с', 'c', name)
    name = re.sub(r'в\/п', 'вп', name)
    name = re.sub(r'х\/дп', 'хдп', name)
    name = re.sub(r'м\/б', 'мб', name)
    name = re.sub(r'тг', 'tg', name)
    name = re.sub(r'пвм', 'пвм', name)
    name = re.sub(r'сн-(\d+)', 'сн\\1', name)
    name = re.sub(r'^\s*сн710\s+', '', name)
    name = re.sub(r'tg\s+столик', 'tgстолик', name)
    name = re.sub(r'пиастра\s+столик', 'пиастрастолик', name)
    name = re.sub(r'пластик\s+хром', 'пластикхром', name)
    name = re.sub(r'\s+', ' ', name).strip()
    return name

# Преобразование пустых значений
def normalize_value(value):
    if isinstance(value, str) and value.strip() in ('', '-', '--'):
        return ""
    if isinstance(value, float) and math.isnan(value):
        return ""
    if value is None:
        return ""
    return str(value)

# Замена точки на запятую в числовых значениях
def format_number(value):
    if isinstance(value, (int, float)):
        return f"{round(value, 2):.2f}".replace('.', ',')
    if isinstance(value, str):
        try:
            num = float(value.replace(',', '.'))
            return f"{round(num, 2):.2f}".replace('.', ',')
        except:
            return value
    return value

def format_number_whole(value):
    if isinstance(value, (int, float)):
        return f"{round(value, 2):.2f}".replace('.', ',')
    if isinstance(value, str):
        try:
            num = float(value.replace(',', '.'))
            return f"{round(num, 2):.0f}".replace('.', ',')
        except:
            return value
    return value

excel_path = r'C:\Users\UTFC\Documents\Downloads\Таблица с размерами (для внутреннего пользования).xlsx'
df = pd.read_excel(excel_path, sheet_name='Размеры')

excel_data = {}
models_excel = df.iloc[3:, 1].dropna().tolist()

columns_mapping = {
    'Unnamed: 2': ('chair_height', 'min', 'max'),
    'Unnamed: 4': ('headrest_height', 'min', 'max'),
    'Unnamed: 6': ('seat_to_floor_height', 'min', 'max'),
    'Unnamed: 8': ('seat_to_floor_height_upper', 'min', 'max'),
    'Unnamed: 10': ('armrest_height_from_floor', 'min', 'max'),
    'Unnamed: 12': ('armrest_height_from_seat', 'min', 'max'),
    'Unnamed: 14': ('armrest_width_support', None, 'max'),
    'Unnamed: 15': ('armrest_length_support', None, 'max'),
    'Unnamed: 17': ('chair_depth', 'min', None),
    'Unnamed: 19': ('seat_depth', 'min', 'max'),
    'Unnamed: 21': ('seat_depth_km', None, 'max'),
    'Unnamed: 22': ('backrest_height', None, 'max'),
    'Unnamed: 23': ('backrest_to_seat_height', 'min', 'max'),
    'Unnamed: 25': ('backrest_height_external', None, 'max'),
    'Unnamed: 27': ('seat_width_with_armrests', 'min', 'max'),
    'Unnamed: 29': ('seat_width', None, 'max'),
    'Unnamed: 30': ('backrest_width_narrow', None, 'max'),
    'Unnamed: 31': ('backrest_width_wide', None, 'max'),
    'Unnamed: 32': ('diameter_cross', None, 'max'),
    'Unnamed: 33': ('runners_width', None, 'max'),
    'Unnamed: 34': ('runners_depth', None, 'max'),
    'Unnamed: 35': ('recommended_load', None, None),
    'Unnamed: 36': ('max_load', None, None),
    'Unnamed: 37': ('skeleton', None, None),
    'Unnamed: 38': ('minpromtorg', None, None),
    'Unnamed: 39': ('netto', None, None),
    'Unnamed: 40': ('brutto', None, None),
    'Unnamed: 41': ('package_width', None, None),
    'Unnamed: 42': ('package_depth', None, None),
    'Unnamed: 43': ('package_height', None, None),
    'Unnamed: 44': ('volume', None, None),
    'Unnamed: 45': ('box_on_pallet', None, None),
    'Unnamed: 46': ('pallet_width', None, None),
}

for i, model in enumerate(models_excel):
    normalized_model = normalize_model_name(model)
    model_data = {
        "model": model,
        "normalized": normalized_model,
        "dimensions_details": {},
        "additional_info": {}
    }

    for col, (key, min_key, max_key) in columns_mapping.items():
        if min_key is not None and max_key is not None:
            model_data["dimensions_details"][key] = {
                "min": format_number_whole(normalize_value(df.iloc[i + 3, df.columns.get_loc(col)])),
                "max": format_number_whole(normalize_value(df.iloc[i + 3, df.columns.get_loc(col) + 1]))
            }
        elif min_key is not None:
            model_data["dimensions_details"][key] = {
                "min": format_number_whole(normalize_value(df.iloc[i + 3, df.columns.get_loc(col)])),
                "max": None
            }
        elif max_key is not None:
            model_data["dimensions_details"][key] = {
                "max": format_number_whole(normalize_value(df.iloc[i + 3, df.columns.get_loc(col)]))
            }
        else:
            model_data["dimensions_details"][key] = format_number_whole(normalize_value(df.iloc[i + 3, df.columns.get_loc(col)]))

    model_data["additional_info"] = {
        "package_dimensions": {
            "width": format_number_whole(normalize_value(df.iloc[i + 3, df.columns.get_loc('Unnamed: 40')])),
            "depth": format_number_whole(normalize_value(df.iloc[i + 3, df.columns.get_loc('Unnamed: 41')])),
            "height": format_number_whole(normalize_value(df.iloc[i + 3, df.columns.get_loc('Unnamed: 42')]))
        },
        "volume": format_number(normalize_value(df.iloc[i + 3, df.columns.get_loc('Unnamed: 44')]))
    }

    excel_data[normalized_model] = model_data

products_dir = r'C:\Users\UTFC\Documents\БалтМебель\to\products'

json_files = []
for root, dirs, files in os.walk(products_dir):
    for file in files:
        if file.endswith('.json'):
            json_files.append(os.path.join(root, file))

missing_in_json = set(excel_data.keys())

all_dimension_params = [
    "chair_height", "headrest_height", "seat_to_floor_height", "armrest_height_from_seat",
    "chair_depth", "seat_depth", "backrest_height", "backrest_to_seat_height",
    "seat_width_with_armrests", "seat_width", "diameter_cross", "runners_width",
    "runners_depth", "seat_to_floor_height_upper", "armrest_height_from_floor",
    "armrest_width_support", "armrest_length_support", "seat_depth_km",
    "backrest_height_external", "backrest_width_narrow", "backrest_width_wide",
    "recommended_load", "max_load", "skeleton", "minpromtorg", "typeofproduct",
    "netto", "brutto", "package_width", "package_depth", "package_height", "volume"
]

failed_updates = []

for json_file in json_files:
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            original_data = json.load(f)

        parents_mapping_normalized = {normalize_model_name(k): v for k, v in parents_mapping.items()}

        model_name = original_data.get('namefile', [''])[0] if isinstance(original_data.get('namefile'), list) else original_data.get('namefile', '')
        if not model_name:
            model_name = original_data.get('name', [''])[0] if isinstance(original_data.get('name'), list) else original_data.get('name', '')

        normalized_name = normalize_model_name(model_name)

        parent_model_name = parents_mapping_normalized.get(normalized_name)

        if parent_model_name and parent_model_name in excel_data:
            parent_data = excel_data[parent_model_name]

            if 'dimensions_details' not in original_data or not original_data.get('dimensions_details'):
                original_data['dimensions_details'] = [{}]

            if isinstance(original_data.get('dimensions_details'), list) and len(original_data['dimensions_details']) > 0:
                dimensions = original_data['dimensions_details'][0]
            else:
                dimensions = {}
                original_data['dimensions_details'] = [dimensions]

            for key, value in parent_data['dimensions_details'].items():
                if key in dimensions:
                    if isinstance(value, dict):
                        for sub_key, sub_value in value.items():
                            if sub_value is not None and sub_value != "":
                                if key not in dimensions:
                                    dimensions[key] = {}
                                dimensions[key][sub_key] = sub_value
                    else:
                        if value is not None and value != "":
                            dimensions[key] = value

            if 'additional_info' in original_data:
                for key, value in parent_data['additional_info'].items():
                    if key in original_data['additional_info']:
                        if isinstance(value, dict):
                            for sub_key, sub_value in value.items():
                                if sub_value is not None and sub_value != "":
                                    original_data['additional_info'][key][sub_key] = sub_value
                        else:
                            if value is not None and value != "":
                                original_data['additional_info'][key] = value

        if 'dimensions_details' not in original_data or not original_data.get('dimensions_details'):
            original_data['dimensions_details'] = [{}]

        if isinstance(original_data.get('dimensions_details'), list) and len(original_data['dimensions_details']) > 0:
            dimensions = original_data['dimensions_details'][0]
        else:
            dimensions = {}
            original_data['dimensions_details'] = [dimensions]

        for param in all_dimension_params:
            if param not in dimensions:
                dimensions[param] = {"min": "", "max": ""}

        if normalized_name in excel_data:
            excel_model_data = excel_data[normalized_name]
            for key, value in excel_model_data['dimensions_details'].items():
                if key in dimensions:
                    if isinstance(value, dict):
                        for sub_key, sub_value in value.items():
                            if sub_value is not None and sub_value != "":
                                if key not in dimensions:
                                    dimensions[key] = {}
                                dimensions[key][sub_key] = sub_value
                    else:
                        if value is not None and value != "":
                            dimensions[key] = value

            if 'additional_info' in original_data:
                if 'package_dimensions' in original_data['additional_info']:
                    for key, value in excel_model_data['additional_info']['package_dimensions'].items():
                        if value is not None and value != "":
                            original_data['additional_info']['package_dimensions'][key] = value
                if 'volume' in original_data['additional_info']:
                    if excel_model_data['additional_info']['volume'] is not None:
                        original_data['additional_info']['volume'] = excel_model_data['additional_info']['volume']

            if 'skeleton' in original_data and excel_model_data['dimensions_details'].get('skeleton') is not None:
                original_data['skeleton'] = excel_model_data['dimensions_details'].get('skeleton')
            if 'minpromtorg' in original_data and excel_model_data['dimensions_details'].get('minpromtorg') is not None:
                original_data['minpromtorg'] = excel_model_data['dimensions_details'].get('minpromtorg')
            if 'typeofproduct' in original_data and excel_model_data['dimensions_details'].get('typeofproduct') is not None:
                original_data['typeofproduct'] = excel_model_data['dimensions_details'].get('typeofproduct')

            if 'guarantee' in original_data and len(original_data['guarantee']) > 0:
                if 'max_load' in original_data['guarantee'][0] and excel_model_data['dimensions_details'].get('max_load') is not None:
                    original_data['guarantee'][0]['max_load'] = format_number_whole(excel_model_data['dimensions_details'].get('max_load'))
                if 'recommended_load' in original_data['guarantee'][0] and excel_model_data['dimensions_details'].get('recommended_load') is not None:
                    original_data['guarantee'][0]['recommended_load'] = format_number_whole(excel_model_data['dimensions_details'].get('recommended_load'))

            if 'dimensions' in original_data and len(original_data['dimensions']) > 0:
                if 'brutto' in original_data['dimensions'][0] and excel_model_data['dimensions_details'].get('brutto') is not None:
                    original_data['dimensions'][0]['brutto'] = format_number(excel_model_data['dimensions_details'].get('brutto'))
                if 'netto' in original_data['dimensions'][0] and excel_model_data['dimensions_details'].get('netto') is not None:
                    original_data['dimensions'][0]['netto'] = format_number(excel_model_data['dimensions_details'].get('netto'))

            if 'dimensions' in original_data and len(original_data['dimensions']) > 0 and excel_model_data['additional_info'].get('volume') is not None:
                original_data['dimensions'][0]['volume'] = format_number(excel_model_data['additional_info'].get('volume'))

        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(original_data, f, ensure_ascii=False, indent=4)

    except Exception as e:
        failed_updates.append((json_file, str(e)))

with open('failed_updates.txt', 'w', encoding='utf-8') as f:
    for file, reason in failed_updates:
        f.write(f"{file}: {reason}\n")

with open('missing_in_json.txt', 'w', encoding='utf-8') as f:
    for model in missing_in_json:
        f.write(f"{model}\n")

print("Обновление завершено. Список неудачных обновлений в failed_updates.txt, отсутствующих моделей в missing_in_json.txt")