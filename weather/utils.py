import requests_cache
from geopy.geocoders import Nominatim
from retry import retry

cache_session = requests_cache.CachedSession('.cache', expire_after=3600)

geolocator = Nominatim(user_agent="weather")

@retry(tries=3, delay=2)
def get_coordinates(city_name):
    location = geolocator.geocode(city_name)
    if location:
        return location.latitude, location.longitude
    else:
        raise ValueError("Нет координат")

@retry(tries=3, delay=2)
def get_weather(city_name):
    latitude, longitude = get_coordinates(city_name)
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m," \
          f"precipitation,wind_speed_10m,relative_humidity_2m"
    response = cache_session.get(url)
    response.raise_for_status()
    return response.json()
