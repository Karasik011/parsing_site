import pandas as pd
import sqlite3
import os

DB_NAME = 'project_data.db'
CSV_FILE = 'for_dashboard.csv'

conn = sqlite3.connect(DB_NAME)

print(">>> Експортуємо дані для Looker Studio...")

# Читаємо нашу майстер-таблицю
df = pd.read_sql("SELECT * FROM Сводная_KWT", conn)

# Додаємо обчислювані поля, щоб в Лукері було легше
# Наприклад: сумарна частота
df['Total_Volume'] = df['Volume_Google'] + df['Volume_Ahrefs']

# Зберігаємо в CSV
df.to_csv(CSV_FILE, index=False)

print(f"✅ Готово! Файл '{CSV_FILE}' створено.")
print("Завантажуй цей файл у Looker Studio.")
conn.close()