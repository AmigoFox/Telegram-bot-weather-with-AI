from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd

# Инициализация драйвера Selenium
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

url = "https://rp5.ru/Погода_в_Ростове-на-Дону"
driver.get(url)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# Находим таблицу
table = soup.find("table", id="forecastTable_1_3")

# Проверка наличия таблицы
if table:
    # Список для хранения данных
    days = []
    times = []
    cloudiness = []
    precipitation = []
    temperature = []
    feels_like = []
    pressure = []
    wind_speed = []
    sunrise_sunset = []
    moonrise_moonset = []

    # Получаем строки таблицы
    rows = table.find_all("tr")

    # Пропускаем первую строку, которая является заголовками
    for row in rows[1:]:
        cols = row.find_all("td")

        # Собираем данные из строки
        data = [col.get_text(strip=True) for col in cols]

        # Проверяем, что данные не пустые и их достаточно для всех параметров
        if len(data) >= 10:  # Убедимся, что строка содержит хотя бы 10 данных
            days.append(data[0])  # День недели или название дня
            times.append(data[1])  # Время
            cloudiness.append(data[2])  # Облачность
            precipitation.append(data[3])  # Осадки
            temperature.append(data[4])  # Температура
            feels_like.append(data[5])  # Ощущаемая температура
            pressure.append(data[6])  # Давление
            wind_speed.append(data[7])  # Скорость ветра
            sunrise_sunset.append(data[8])  # Восход/заход солнца
            moonrise_moonset.append(data[9] if len(data) > 9 else '')  # Восход/заход Луны

else:
    print("Таблица не найдена")

# Закрытие драйвера
driver.quit()

# Создаем DataFrame для удобного отображения
weather_data = pd.DataFrame({
    "День": days,
    "Время": times,
    "Облачность": cloudiness,
    "Осадки (мм)": precipitation,
    "Температура (°C)": temperature,
    "Ощущается как (°C)": feels_like,
    "Давление (мм рт. ст)": pressure,
    "Ветер (м/с)": wind_speed,
    "Восход солнца": sunrise_sunset,
    "Заход солнца": moonrise_moonset
})

# Отображаем таблицу
print(weather_data)

# Если нужно сохранить в файл, можно использовать:
# weather_data.to_csv("weather_forecast.csv", index=False)
