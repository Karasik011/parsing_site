import pandas as pd
import re


def get_shadow_key(text):
    if not isinstance(text, str): return ""
    key = text.lower()
    key = re.sub(r'\.co\.uk|\.nl|\.com|\.net|\.org|\.eu', '', key)
    stop_words = r'\b(casino|online|mobile|app|uk|nl|ca|nz|au|official|site)\b'
    key = re.sub(stop_words, '', key)
    key = re.sub(r'[^\w]', '', key)
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
    output_file = 'cleared_dataset.csv'

    try:
        df = pd.read_csv(input_file)
        df['ShadowKey'] = df['Casino Name'].apply(get_shadow_key)
        df = df[df['ShadowKey'] != ""]
        df['Score'] = df['Casino Name'].apply(get_quality_score)
        df = df.sort_values(by='Score')
        duplicates = df[df.duplicated(subset=['ShadowKey'], keep='first')]
        if not duplicates.empty:
            numeric_dups = df[df['Casino Name'].str.match(r'^\d+$', na=False)]
            found = duplicates[duplicates['Casino Name'].str.match(r'^\d+$')]

            for index, row in found.head(5).iterrows():
                survivor = df[df['ShadowKey'] == row['ShadowKey']].iloc[0]['Casino Name']
        df_clean = df.drop_duplicates(subset=['ShadowKey'], keep='first').copy()
        final_df = df_clean[['Casino Name']].sort_values(by='Casino Name')

        final_df.to_csv(output_file, index=False)
        print(f"\nГотово! Збережено у: {output_file}")
        print(f"Всього казино: {len(final_df)}")

    except FileNotFoundError:
        print("Файл не знайдено!")


if __name__ == "__main__":
    main()