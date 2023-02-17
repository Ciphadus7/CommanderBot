import requests
from dotenv import load_dotenv
import os
load_dotenv()

API_KEY = os.getenv("API_KEY_WEATHER")

def get_weather_single(*args, API_KEY=API_KEY):
    city = str(*args)
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    r = requests.get(url)
    content = r.json()
    print(content)
    temperature = content['main']['temp']
    print(temperature)
    # condition = content['weather'][0]['description']

    return f'Current temperature in {(city).title()} is {temperature}℃.'

