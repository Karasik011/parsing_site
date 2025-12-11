import time
import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def parse_guru_final():
    print("--- [3/3] ЗАПУСК ОКРЕМОГО ПАРСЕРА CASINO GURU ---")

    options = webdriver.ChromeOptions()
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    guru_names = []

    try:
        url = "https://casino.guru/top-online-casinos"
        driver.get(url)
        time.sleep(5)

        try:
            print("Тисну вкладку 'All'...")
            all_tab = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'label[data-tab-name="ALL"]'))
            )
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", all_tab)
            driver.execute_script("arguments[0].click();", all_tab)
            time.sleep(5)
        except Exception as e:
            print(f"Увага: Не вдалося клікнути 'All' (можливо, вже активно): {e}")
        print("Починаю розкривати весь список...")
        clicks = 0
        while True:
            try:
                load_more_btn = driver.find_element(By.CSS_SELECTOR, ".load-more-results")

                if not load_more_btn.is_displayed():
                    break

                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", load_more_btn)
                driver.execute_script("arguments[0].click();", load_more_btn)
                clicks += 1
                time.sleep(2.5)
            except:
                break

        print(f"Список розкрито (кліків: {clicks}).")
        print("Збираю назви...")
        card_headings = driver.find_elements(By.CSS_SELECTOR, ".casino-card-heading h3")

        for h3 in card_headings:
            text = h3.text.strip()
            if text:
                guru_names.append(text)

        print(f"Знайдено казино на Guru: {len(guru_names)}")

    except Exception as e:
        print(f"Помилка: {e}")
    finally:
        driver.quit()
    if guru_names:
        filename = 'all_casinos_combined.csv'

        df_new = pd.DataFrame(guru_names, columns=['Casino Name'])
        file_exists = os.path.isfile(filename)
        df_new.to_csv(filename, mode='a', header=not file_exists, index=False)

        print(f"Успішно додано {len(guru_names)} рядків у файл {filename}")
    else:
        print("Список порожній, нічого не додано.")


if __name__ == "__main__":
    parse_guru_final()