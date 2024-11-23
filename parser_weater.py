from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
url = "https://rp5.ru/Погода_в_Ростове-на-Дону"
driver.get(url)

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# Находим все ячейки с классом "forecastTable_1_3"
links = soup.find_all("td", class_="forecastTable_1_3")

# Ищем ссылки в ячейках и проходим по каждому элементу
found = []
for x in links:
    siblings = x.find_next_siblings("td")
    # Добавляем ссылки из всех найденных соседних ячеек
    for sibling in siblings:
        link = sibling.find("a")
        if link:  # Проверяем, что ссылка существует
            found.append(link)

print(found)

driver.quit()
