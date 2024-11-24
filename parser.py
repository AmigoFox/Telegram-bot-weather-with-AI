from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

url = "https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D0%B3%D0%BE%D1%80%D0%BE%D0%B4%D0%BE%D0%B2_%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D0%B8"
driver.get(url)

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

links = soup.find('table', class_='standard sortable jquery-tablesorter')
print(links)


if links :
    rows = links.find_all("tr")
    for row in rows:
        cols = row.find_all("td")
        data = [col.get_text(strip=True) for col in cols]
        if data:
            print(data[2])
else:
    print("Таблица не найдена")
'''
with open("name_city.txt", "a", encoding="utf-8") as file:
    for link in links:
        href = link['href']

        if href.startswith('/'):
            city_name = href.split('/Погода_в_')[-1]  
            print(city_name)
            file.write(city_name + "\n")
            print(city_name)
'''

driver.quit()