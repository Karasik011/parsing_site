import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
import os as os
all_casinos = []

options = webdriver.ChromeOptions()
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

url_1 = "https://www.gambling.com/uk/online-casinos"
print(f"\n--- [1/2] Обробка: {url_1} ---")
try:
    driver.get(url_1)
    time.sleep(3)

    print("Розкриваю список...")
    while True:
        try:
            xpath_query = "//a[contains(@class, 'automation-readmore-button') and contains(., 'Show More')]"
            more_button = driver.find_element(By.XPATH, xpath_query)
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", more_button)
            driver.execute_script("arguments[0].click();", more_button)
            time.sleep(2)
        except NoSuchElementException:
            break
        except Exception:
            break

    elements_1 = driver.find_elements(By.XPATH, '//li[@data-product]')
    for el in elements_1:
        name = el.get_attribute("data-product")
        if name:
            all_casinos.append(name)
    print(f"Знайдено: {len(elements_1)}")
except Exception as e:
    print(f"Помилка на сайті 1: {e}")

url_2 = "https://www.top10casino.nl/casinos"
print(f"\n--- [2/2] Обробка: {url_2} ---")

driver.quit()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    driver.get(url_2)
    time.sleep(4)
    print(f"Заголовок: {driver.title}")

    print("Починаю плавну прокрутку...")

    total_height = driver.execute_script("return document.body.scrollHeight")
    for i in range(0, total_height + 3000, 700):
        driver.execute_script(f"window.scrollTo(0, {i});")
        time.sleep(0.3)
        new_total_height = driver.execute_script("return document.body.scrollHeight")
        if new_total_height > total_height:
            total_height = new_total_height

    time.sleep(2)
    elements_2 = driver.find_elements(By.CSS_SELECTOR, "div.cl-name")

    count_2 = 0
    for el in elements_2:
        name = el.get_attribute("textContent").strip()
        if name:
            all_casinos.append(name)
            count_2 += 1

    print(f"Знайдено: {count_2}")

except Exception as e:
    print(f"Помилка на сайті 2: {e}")
finally:
    driver.quit()
if all_casinos:
    df = pd.DataFrame(all_casinos, columns=['Casino Name'])
    df = df.drop_duplicates(subset=['Casino Name'], keep='first')
    df = df.reset_index(drop=True)

    print(f"\nВСЬОГО УНІКАЛЬНИХ: {len(df)}")
    print(df.head(10))
    df.to_csv('all_casinos_combined.csv', mode='a', header=not os.path.isfile('all_casinos_combined.csv'), index=False)
else:
    print("\nНа жаль, список порожній.")
