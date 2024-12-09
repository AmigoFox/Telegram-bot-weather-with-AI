import requests
import python_weather
import asyncio
import os
import re
'''
def get_weather(city, api_key):
    url = f'https://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&lang=ru'
    response = requests.get(url)
    data = response.json()
    if 'error' not in data:
        temp = data['current']['temp_c']
        humidity = data['current']['humidity']
        wind_speed = data['current']['wind_kph']
        condition = data['current']['condition']['text']
        return f'Погода в городе {city}: {temp}°C, {condition}, влажность: {humidity}%, ветер: {wind_speed} км/ч.'
    else:
        return f'Не удалось получить данные для города {city}.'

api_key = '29c4ed5f56c04c3db8090820240912'
city = 'Ростов-на-Дону'
print(get_weather(city, api_key))
'''

async def getweather() -> None:
    text_weather = []
    # declare the client. the measuring unit used defaults to the metric system (celcius, km/h, etc.)
    async with python_weather.Client(unit=python_weather.METRIC) as client:
        # fetch a weather forecast from a city
        weather = await client.get('Ростов-на-Дону')

        # returns the current day's forecast temperature (int)
        #print(weather.temperature)

        # get the weather forecast for a few days
        for daily in weather:
            #print(daily)
            text_weather.append(daily)

            # hourly forecasts
            for hourly in daily:
                #print(f' --> {hourly!r}')
                text_weather.append(hourly)
    #print(text_weather,'\n')
    fin_info_weather = []
    for i in text_weather:
        parts = re.split(r'\s+|[.]', str(i))
        print(parts)
        for part in parts:
            print(part,'это партсы')




if __name__ == '__main__':
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(getweather())