from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

weater_table = np.array([])

url = "https://rp5.ru/Погода_в_Ростове-на-Дону"
driver.get(url)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
table = soup.find("table", id="forecastTable_1_3")

if table:
    rows = table.find_all("tr")
    for row in rows:
        cols = row.find_all("td")
        data = [col.get_text(strip=True) for col in cols]
        if data:
            print(data)
else:
    print("Таблица не найдена")
driver.quit()