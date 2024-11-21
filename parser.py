from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Открываем страницу
url = "https://rp5.ru/Погода_в_России"
driver.get(url)

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

links = soup.find_all('a', href=True)

with open("name_city.txt", "a", encoding="utf-8") as file:
    for link in links:
        href = link['href']

        if href.startswith('/'):
            city_name = href.split('/Погода_в_')[-1]  
            print(city_name)
            file.write(city_name + "\n")
            print(city_name)


driver.quit()