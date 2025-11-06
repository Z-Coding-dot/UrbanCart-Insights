from prometheus_client import start_http_server, Gauge
import requests, time

API_KEY = "9236930e832a0e0c577adb449dfea0f3"
CITIES = ["Astana", "Almaty", "London"]

# Define metrics with label
temperature = Gauge('weather_temperature_celsius', 'Current temperature in Celsius', ['city'])
humidity = Gauge('weather_humidity_percent', 'Current humidity in percent', ['city'])
pressure = Gauge('weather_pressure_hpa', 'Atmospheric pressure in hPa', ['city'])
wind_speed = Gauge('weather_wind_speed_mps', 'Wind speed in m/s', ['city'])
clouds = Gauge('weather_clouds_percent', 'Cloudiness percent', ['city'])
visibility = Gauge('weather_visibility_m', 'Visibility in meters', ['city'])
feels_like = Gauge('weather_feels_like_celsius', 'Feels like temperature', ['city'])
sunrise = Gauge('weather_sunrise_unix', 'Sunrise time (UNIX)', ['city'])
sunset = Gauge('weather_sunset_unix', 'Sunset time (UNIX)', ['city'])
temp_diff = Gauge('weather_temp_difference', 'Difference between temp and feels_like', ['city'])

def fetch_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    print(f"Fetching data for {city} ...")
    r = requests.get(url)
    if r.status_code != 200:
        print(f"Error fetching {city}: {r.status_code} {r.text}")
        return

    data = r.json()
    if 'main' not in data:
        print(f"Invalid data for {city}: {data}")
        return

    print(f"{city} temp: {data['main']['temp']} °C")
    temperature.labels(city=city).set(data['main']['temp'])
    humidity.labels(city=city).set(data['main']['humidity'])
    pressure.labels(city=city).set(data['main']['pressure'])
    wind_speed.labels(city=city).set(data['wind']['speed'])
    clouds.labels(city=city).set(data['clouds']['all'])
    visibility.labels(city=city).set(data.get('visibility', 0))
    feels_like.labels(city=city).set(data['main']['feels_like'])
    sunrise.labels(city=city).set(data['sys']['sunrise'])
    sunset.labels(city=city).set(data['sys']['sunset'])
    temp_diff.labels(city=city).set(data['main']['temp'] - data['main']['feels_like'])

if __name__ == "__main__":
    print("Starting exporter on port 8010...")
    start_http_server(8010)
    while True:
        for city in CITIES:
            fetch_weather(city)
        print("Cycle complete. Sleeping 20s...\n")
        time.sleep(20)





# How to run (docker-compose up -d)
# Load Simulation for CPU TEST
# docker run --rm -it alpine sh -c "while true; do cat /dev/zero > /dev/null; done"
# Access to Dashboard : localhost:3000
# Prometheus URL (localhost:9090)
# http://localhost:9090/targets