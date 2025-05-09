from flask import Flask, render_template, request
import requests
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('API_KEY')

app = Flask(__name__)

def get_lat_lon(city_name, country_code, API_key):
    resp = requests.get(
        f'http://api.openweathermap.org/geo/1.0/direct?q={city_name},{country_code}&limit=1&appid={API_key}'
    )
    data = resp.json()
    if data:
        return data[0]['lat'], data[0]['lon']
    return None, None

@app.route('/', methods=['GET', 'POST'])
def index():
    weather = None
    lang = 'en'
    weather_type = None

    if request.method == 'POST':
        city = request.form['city']
        country = request.form['country']
        lang = request.form['lang']

        lat, lon = get_lat_lon(city, country, api_key)

        if lat and lon:
            url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang={lang}'
            resp = requests.get(url)
            if resp.status_code == 200:
                data = resp.json()
                weather_type = data['weather'][0]['main']
                weather = {
                    'city': data['name'],
                    'description': data['weather'][0]['description'],
                    'temperature': data['main']['temp'],
                    'humidity': data['main']['humidity'],
                    'wind_speed': data['wind']['speed'],
                }

    return render_template('index.html', weather=weather, lang=lang, weather_type=weather_type)

if __name__ == '__main__':
    app.run(debug=True)
