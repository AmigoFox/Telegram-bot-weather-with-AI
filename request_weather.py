import python_weather
import re
import asyncio
import os

def weather():
    info_weather = []
    async def getweather() -> None:
        # declare the client. the measuring unit used defaults to the metric system (celcius, km/h, etc.)
        async with python_weather.Client(unit=python_weather.METRIC) as client:
            # fetch a weather forecast from a city
            weather = await client.get('Москва')

            # returns the current day's forecast temperature (int)
            print(weather.temperature)

            # get the weather forecast for a few days
            for daily in weather:
                print(daily)
                info_weather.append(daily)
            print(info_weather)
            list = []
            SPLIT_PATTERN = r'[;,().<>]DailyForecast date=datetime datetemperature'
            for i in info_weather:
                parts = re.split(SPLIT_PATTERN, i)
                list.append(parts)
            for j in list:
                print(j)

                # hourly forecasts
                #for hourly in daily:
                #   print(f' --> {hourly!r}')


    if __name__ == '__main__':
        # see https://stackoverflow.com/questions/45600579/asyncio-event-loop-is-closed-when-getting-loop
        # for more details
        if os.name == 'nt':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

        asyncio.run(getweather())
    return info_weather
weather()