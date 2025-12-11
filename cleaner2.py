import pandas as pd
import re


def is_junk(text):
    if not isinstance(text, str):
        return True

    text_lower = text.lower()
    if "http" in text_lower or "www." in text_lower or ".html" in text_lower:
        return True
    if "@" in text_lower and "." in text_lower:
        return True
    if len(text.strip()) < 2:
        return True

    return False


def clean_visual_name(text):

    if not isinstance(text, str):
        return ""
    text = re.sub(r'[-_]', ' ', text)
    domains = r'\.(bet|io|com|net|org|eu|nl|sk|lv|cz|pl|de|se|uk|ca|biz|info|me)\b'
    text = re.sub(domains, '', text, flags=re.IGNORECASE)

    # Прибираємо зайві пробіли, що могли утворитися
    text = re.sub(r'\s+', ' ', text).strip()

    return text


def get_shadow_key(text):
    """Створює ключ для пошуку дублікатів (агресивна нормалізація)."""
    if not isinstance(text, str):
        return ""

    key = text.lower().strip()
    key = re.sub(r'\.[a-z0-9]{2,5}', '', key)
    remove_chunks = [
        "casino", "online", "bet", "play", "gaming", "slot", "slots",
        "book", "wager", "club", "games", "mobile"
    ]
    for chunk in remove_chunks:
        key = re.sub(rf'\b{chunk}\b', '', key)
    key = re.sub(r'[^a-z0-9]', '', key)

    return key


def get_quality_score(name):
    clean = name.strip()
    if re.fullmatch(r'\d+', clean):
        return 1000
    if len(clean) < 3:
        return 900
    return len(clean)


def main():
    input_file = 'all_casinos_combined.csv'
    output_file = 'cleared_dataset_v2.csv'

    try:
        df = pd.read_csv(input_file)
        print(f"Всього записів на вході: {len(df)}")
        df = df[~df['Casino Name'].apply(is_junk)].copy()
        print(f"Після видалення URL та пошт: {len(df)}")
        df['Casino Name'] = df['Casino Name'].apply(clean_visual_name)
        df['ShadowKey'] = df['Casino Name'].apply(get_shadow_key)
        df = df[df['ShadowKey'] != ""].copy()
        df['Score'] = df['Casino Name'].apply(get_quality_score)
        df = df.sort_values(by='Score')
        df_clean = df.drop_duplicates(subset=['ShadowKey'], keep='first').copy()
        final_df = df_clean[['Casino Name']].sort_values(by='Casino Name')

        print(f"Фінальна кількість чистих казино: {len(final_df)}")
        print(f"Всього видалено: {len(pd.read_csv(input_file)) - len(final_df)}")

        final_df.to_csv(output_file, index=False)
        print(f"\nГотово! Збережено у: {output_file}")

    except FileNotFoundError:
        print("Файл не знайдено! Перевір назву.")


if __name__ == "__main__":
    main()