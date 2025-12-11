import pandas as pd
import sqlite3
import os

DB_NAME = 'project_data.db'
home_folder = os.path.expanduser("~")
excel_file = os.path.join(home_folder, "Downloads", "Бренды.xlsx")

EXCLUDED_EXACT = ['ТЗ', 'To-Do', 'Підсумок експорту']

if os.path.exists(DB_NAME):
    os.remove(DB_NAME)
conn = sqlite3.connect(DB_NAME)
def clean_value(x):
    if pd.isna(x): return 0
    s = str(x).strip()
    if s in ['-', 'nan', '', 'None']: return 0
    s = s.replace('%', '').replace(' ', '').replace(',', '.')
    try:
        return float(s) if '.' in s else int(s)
    except:
        return s

def clean_header(val):
    if pd.isna(val): return ""
    return str(val).strip().replace(" ", "")

print(f">>> Працюємо з файлом: {excel_file}")

try:
    print("🔹 Обробка: Бренды")
    df_raw = pd.read_excel(excel_file, sheet_name='Бренды', header=None)
    row_tiers = df_raw.iloc[0].ffill()
    row_codes = df_raw.iloc[2]
    new_cols = ["Brand", "Total_Sites"]
    for i in range(2, len(row_codes)):
        c = clean_header(row_codes[i])
        t = clean_header(row_tiers[i])
        if c and c not in ['nan', '0', '-']:
            new_cols.append(f"{c}_{t}_Sites")
        else:
            new_cols.append(f"Drop_{i}")

    df = df_raw.iloc[3:].copy()
    df = df.iloc[:, :len(new_cols)]
    df.columns = new_cols
    df = df[[c for c in df.columns if not c.startswith('Drop')]]
    df.map(clean_value).to_sql('brands', conn, if_exists='replace', index=False)

    print("🔹 Обробка: Сводная_Trends")
    df_raw = pd.read_excel(excel_file, sheet_name='Сводная_Trends', header=None)
    row_tiers = df_raw.iloc[0].ffill()
    row_codes = df_raw.iloc[2]
    new_cols = ["Brand", "Keyword", "Projects"]
    for i in range(3, len(row_codes)):
        c = clean_header(row_codes[i])
        t = clean_header(row_tiers[i])
        if c and c not in ['nan', '0']:
            new_cols.append(f"{c}_{t}_Trend")
        else:
            new_cols.append(f"Drop_{i}")

    df = df_raw.iloc[3:].copy()
    df = df.iloc[:, :len(new_cols)]
    df.columns = new_cols
    df = df[[c for c in df.columns if not c.startswith('Drop')]]
    df.map(clean_value).to_sql('trends', conn, if_exists='replace', index=False)

    print("🔹 Обробка: Сводная_GAds Ahrefs")
    df_raw = pd.read_excel(excel_file, sheet_name='Сводная_GAds Ahrefs', header=None)
    row_tiers = df_raw.iloc[0].ffill()
    row_countries = df_raw.iloc[2].ffill()
    row_sources = df_raw.iloc[3]

    new_cols = ["Brand", "Keyword", "Projects"]
    for i in range(3, len(row_sources)):
        t = clean_header(row_tiers[i])
        c = clean_header(row_countries[i])
        s = clean_header(row_sources[i])
        if s in ['Google', 'Ahrefs']:
            new_cols.append(f"{c}_{t}_{s}")
        else:
            new_cols.append(f"Drop_{i}")

    df = df_raw.iloc[4:].copy()  # Дані з 5-го рядка
    df = df.iloc[:, :len(new_cols)]
    df.columns = new_cols
    df = df[[c for c in df.columns if not c.startswith('Drop')]]
    df.map(clean_value).to_sql('gads_ahrefs', conn, if_exists='replace', index=False)

    xls = pd.ExcelFile(excel_file)
    for sheet in xls.sheet_names:
        if sheet in ['Бренды', 'Сводная_Trends', 'Сводная_GAds Ahrefs']: continue  # Вже взяли
        if sheet in EXCLUDED_EXACT: continue  # Сміття

        print(f"🔹 Додаткова таблиця: {sheet}")
        df = pd.read_excel(excel_file, sheet_name=sheet)  # Читаємо як просту таблицю
        df.map(clean_value).to_sql(sheet, conn, if_exists='replace', index=False)

except Exception as e:
    print(f"❌ ПОМИЛКА: {e}")

conn.close()
print(f"\n✅ ГОТОВО. Файл бази: {DB_NAME}")