import os
import pandas as pd

base_path = os.path.dirname(os.path.abspath(__file__))
assets_path = f"{base_path}/assets"
out_path = f"{base_path}/out"

# Пути к файлам
file_path = f"{assets_path}/train.xlsx"

# Загрузка данных из файла Train.xlsx
xls = pd.ExcelFile(file_path)

# Чтение данных из листов "economy" и "business"
df_economy = pd.read_excel(xls, "economy")
df_business = pd.read_excel(xls, "business")

# Добавление столбца "class" с соответствующим значением
df_economy["class"] = "economy"
df_business["class"] = "business"

# Объединение данных в один датафрейм
df_combined = pd.concat([df_economy, df_business])

# Функция для преобразования времени в минуты
def time_to_minutes(time_str):
    try:
        hours, minutes = map(int, time_str.split(":"))
        return hours * 60 + minutes
    except (ValueError, IndexError):
        return None

# Удаление дубликатов одновременно по столбцам "airline", "from", "to", "price"
df_combined.drop_duplicates(subset=["airline", "from", "to", "price"], keep="first", inplace=True)

# Преобразование столбца "date" в формат даты
df_combined["date"] = pd.to_datetime(df_combined["date"], format="%d-%m-%Y", errors="coerce")

# Извлечение месяца из даты
df_combined["date"] = df_combined["date"].dt.month

# Фильтрация по заданным значениям в столбце "airline"
valid_airlines = ["Vistara", "Air India", "GO FIRST", "Indigo", "SpiceJet", "AirAsia", "StarAir", "Trujet"]
df_combined = df_combined[df_combined["airline"].isin(valid_airlines)]

# Создание словаря для сопоставления авиакомпаний и их ID
airline_to_id = {
    "Vistara": 1,
    "Air India": 2,
    "Indigo": 3,
    "GO FIRST": 4,
    "AirAsia": 5,
    "SpiceJet": 6,
    "StarAir": 7,
    "Trujet": 8
}

# Присвоение ID каждой авиакомпании
df_combined["airline"] = df_combined["airline"].map(airline_to_id)

# Фильтрация по заданным значениям в столбце "ch_code"
valid_ch_code = ["AI", "UK", "6E", "G8", "I5", "SG", "S5", "2T"]
df_combined = df_combined[df_combined["ch_code"].isin(valid_ch_code)]

# Создание словаря для сопоставления авиакомпаний и их ID
ch_code_to_id = {
    "UK": 1,
    "AI": 2,
    "6E": 3,
    "G8": 4,
    "I5": 5,
    "SG": 6,
    "S5": 7,
    "2T": 8
}

# Присвоение ID каждой авиакомпании
df_combined["ch_code"] = df_combined["ch_code"].map(ch_code_to_id)

# Применение функции к столбцу "arr_time"
df_combined["arr_time"] = df_combined["arr_time"].apply(time_to_minutes)

# Применение функции к столбцу "dep_time"
df_combined["dep_time"] = df_combined["dep_time"].apply(time_to_minutes)

# Функция для обработки столбца "stop"
df_combined["stop"] = df_combined["stop"].str.strip()
def process_stop(row):
    if row["stop"] == "non-stop":
        return 0
    elif row["stop"] == "1-stop":
        return 1
    elif row["stop"] == "2+-stop":
        return 2

# Применение функции к столбцу "stop"
df_combined["stop"] = df_combined.apply(process_stop, axis=1)
    
# Функция для преобразования времени в минуты
def time_to_minutes(time_str):
    try:
        hours, minutes = map(int, time_str.replace("h", "").replace("m", "").split())
        return hours * 60 + minutes
    except (ValueError, IndexError):
        return None

# Применение функции к столбцу "time_taken"
df_combined["time_taken"] = df_combined["time_taken"].apply(time_to_minutes)

# Удаление строк, в которых значение столбца "stop" не соответствует условиям
df_combined = df_combined.dropna(subset=["stop"])

# Фильтрация по заданным значениям в столбце "from"
valid_from = ["Delhi", "Mumbai", "Kolkata", "Bangalore", "Hyderabad", "Chennai"]
df_combined = df_combined[df_combined["from"].isin(valid_from)]

# Удаление строк, в которых значения в столбце "from" не соответствуют заданным авиакомпаниям
df_combined = df_combined.dropna(subset=["from"])

# Создание словаря для сопоставления авиакомпаний и их ID
from_to_id = {
    "Delhi": 1,
    "Mumbai": 2,
    "Kolkata": 3,
    "Bangalore": 4,
    "Hyderabad": 5,
    "Chennai": 6,
}

# Присвоение ID 
df_combined["from"] = df_combined["from"].map(from_to_id)

# Фильтрация по заданным значениям в столбце "to"
valid_to = ["Delhi", "Mumbai", "Kolkata", "Bangalore", "Hyderabad", "Chennai"]
df_combined = df_combined[df_combined["to"].isin(valid_to)]

# Удаление строк, в которых значения в столбце "from" не соответствуют заданным авиакомпаниям
df_combined = df_combined.dropna(subset=["to"])

# Создание словаря для сопоставления авиакомпаний и их ID
to_to_id = {
    "Delhi": 1,
    "Mumbai": 2,
    "Kolkata": 3,
    "Bangalore": 4,
    "Hyderabad": 5,
    "Chennai": 6,
}

# Присвоение ID 
df_combined["to"] = df_combined["to"].map(to_to_id)

# Удаление столбца num_code
df_combined.drop(columns=["num_code"], inplace=True)

# Удаление столбца ch_code
df_combined.drop(columns=["ch_code"], inplace=True)

# Функция для обработки столбца "class"
def process_class(row):
    if row["class"] == "economy":
        return 0
    elif row["class"] == "business":
        return 1
    else:
        return row["class"]

# Применение функции к столбцу "class"
df_combined["class"] = df_combined.apply(process_class, axis=1)

# Обработка столбца "price"
df_combined["price"] = df_combined["price"].str.replace(",", "").astype(int)

df_combined.to_excel(f"{out_path}/processing.xlsx", index=False)

print("Обработка завершена")
