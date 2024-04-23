import os
import requests
from dotenv import load_dotenv
from pprint import pprint
from datetime import datetime
load_dotenv()
API_KEY = os.getenv("API_KEY")

def get_weather(city):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=ru"
        response = requests.get(url)
        data = response.json()
        if data['cod'] == 200:
            return data
    except Exception as e:
        return None

# pprint(get_weather('Almaty'))
def get_forecast(city):
    weather_al  = get_weather(city)
    if weather_al is None:
        return None

    sunrise = datetime.fromtimestamp(weather_al['sys']['sunrise'])
    sunset = datetime.fromtimestamp(weather_al['sys']['sunset'])
    long_of_dau = sunset - sunrise




    text =  f"Погода в городе {weather_al['name']}: \n"\
            f"Температура: {weather_al['main']['temp']}°C\n"\
            f"Ощущается как: {weather_al['main']['feels_like']}°C\n"\
            f"Скорость ветра: {weather_al['wind']['speed']} м/с\n"\
            f"Направление ветра: {weather_al['wind']['deg']}°\n"\
            f"Давление: {weather_al['main']['pressure']} мм.рт.ст\n"\
            f"Влажность: {weather_al['main']['humidity']}%\n"\
            f"Облачность: {weather_al['clouds']['all']}%\n"\
            f"Время рассвета: {sunrise.strftime('%H:%M:%S')}\n"\
            f"Время заката: {sunset.strftime('%H:%M:%S')}\n"\
            f'Длительность дня {long_of_dau}'

    return text

def get_weekly_forecast(city):
    try:
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric&lang=ru"
        response = requests.get(url)
        data = response.json()
        if data['cod'] == '200':
            return data
        else:
            print("Ошибка при получении данных:", data['message'])
            return None
    except Exception as e:
        print("Ошибка при запросе API:", e)
        return None


def format_weekly_forecast(data):
    city_name = data['city']['name']
    forecast_list = data['list']
    formatted_forecast = []
    today = None
    today_info = ''
    for forecast in forecast_list:
        date_time = datetime.fromtimestamp(forecast['dt'])
        temperature = forecast['main']['temp']
        feels_like = forecast['main']['feels_like']
        weather_description = forecast['weather'][0]['description']
        if date_time.date() != today:
            today = date_time.date()
            if today_info != '':
                formatted_forecast.append(today_info)
            today_info = f"Дата: {today}\n"
        today_info += f"Дата и время: {date_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        today_info += f"Температура: {temperature}°C, ощущается как: {feels_like}°C\n"
        today_info += f"Погодные условия: {weather_description}\n\n"
    return formatted_forecast

def get_and_format_weekly_forecast(city):
    data = get_weekly_forecast(city)
    if data:
        formatted_forecast = format_weekly_forecast(data)
        return formatted_forecast
    else:
        return "Не удалось получить прогноз погоды на неделю."

# print(get_and_format_weekly_forecast('Almaty'))

            