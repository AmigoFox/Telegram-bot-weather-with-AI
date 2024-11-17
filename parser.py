from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# Инициализация драйвера Selenium
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Открываем страницу
url = "https://rp5.ru/Погода_в_России"
driver.get(url)

# Даем время для загрузки контента (можно заменить на явные ожидания, если нужно)
driver.implicitly_wait(10)

# Получаем HTML-код страницы после загрузки
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# Поиск всех тегов <a> с атрибутом href
links = soup.find_all('a', href=True)

# Открытие файла для записи всех ссылок
with open("city.txt", "a", encoding="utf-8") as file:
    # Печать и запись всех ссылок
    for link in links:
        href = link['href']

        # Если ссылка не абсолютная, делаем её абсолютной
        if not href.startswith('http'):
            href = "https://rp5.ru" + href

        # Записываем ссылку в файл
        file.write(href + "\n")

        # Печатаем ссылку (по желанию)
        print(href)

# Закрываем браузер
driver.quit()
