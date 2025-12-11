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
    print("--- ЗАПУСК ПАРСЕРА CASINO GURU З ПАГІНАЦІЄЮ ---")

    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 15)

    guru_names = []

    try:
        url = "https://casino.guru/top-online-casinos"
        driver.get(url)
        time.sleep(3)
        try:
            print("Тисну 'All'...")
            all_tab = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'label[data-tab-name="ALL"]'))
            )
            driver.execute_script("arguments[0].click();", all_tab)
            time.sleep(3)
        except:
            print("Не вдалося натиснути All (можливо, вже активна).")
        max_pages_elem = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".paging-goto-wrapper span b"))
        )
        max_pages = int(max_pages_elem.text.strip())
        print(f"Виявлено сторінок: {max_pages}")

        current_page = 1

        while current_page <= max_pages:

            print(f"Збираю дані зі сторінки {current_page}/{max_pages}...")
            wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".casino-card-heading h3"))
            )
            time.sleep(1)
            cards = driver.find_elements(By.CSS_SELECTOR, ".casino-card-heading h3")
            page_items = 0

            for h3 in cards:
                try:
                    text = h3.text.strip()
                    if text:
                        guru_names.append(text)
                        page_items += 1
                except:
                    continue

            print(f"  -> зібрано {page_items} казино")
            if current_page < max_pages:
                try:
                    page_input = wait.until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "input.js-paging-goto"))
                    )

                    driver.execute_script("arguments[0].value='';", page_input)
                    page_input.clear()
                    page_input.send_keys(str(current_page + 1))
                    goto_btn = wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "span.js-paging-goto-btn"))
                    )
                    driver.execute_script("arguments[0].click();", goto_btn)
                    time.sleep(2)

                except Exception as e:
                    print(f"Помилка переходу на наступну сторінку: {e}")
                    break

            current_page += 1

        print(f"Усього зібрано: {len(guru_names)} казино")

    except Exception as e:
        print(f"Помилка виконання: {e}")

    finally:
        driver.quit()
    if guru_names:
        filename = "all_casinos_combined.csv"
        df_new = pd.DataFrame(guru_names, columns=["Casino Name"])
        file_exists = os.path.isfile(filename)
        df_new.to_csv(filename, mode='a', header=not file_exists, index=False)
        print(f"Збережено {len(guru_names)} рядків у {filename}")
    else:
        print("Список казино порожній. Нічого не збережено.")


if __name__ == "__main__":
    parse_guru_final()






