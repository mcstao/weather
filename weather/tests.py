from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch

class WeatherTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.index_url = reverse('index')
        self.history_url = reverse('history')
        self.autocomplete_url = reverse('autocomplete')

    @patch('weather.utils.get_weather')
    def test_index_view_post(self, mock_get_weather):
        mock_get_weather.return_value = {'city': 'Париж'}
        response = self.client.post(self.index_url, {'city': 'Париж'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertContains(response, 'Париж')


    def test_history_view(self):
        response = self.client.get(self.history_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'history.html')

    @patch('weather.views.requests.get')
    def test_autocomplete_view(self, mock_get):
        mock_get.return_value.json.return_value = {'geonames': [{'name': 'Париж'}]}
        response = self.client.get(self.autocomplete_url, {'term': 'Пар'})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, ['Париж'])

    @patch('weather.utils.geolocator.geocode')
    def test_get_coordinates(self, mock_geocode):
        from .utils import get_coordinates
        mock_geocode.return_value = type('Location', (object,), {'latitude': 48.86, 'longitude': 2.3399997})()
        latitude, longitude = get_coordinates('Париж')
        print(get_coordinates)
        self.assertEqual(latitude, 48.86)
        self.assertEqual(longitude, 2.3399997)

    @patch('weather.utils.get_coordinates')
    @patch('weather.utils.cache_session.get')
    def test_get_weather(self, mock_get, mock_get_coordinates):
        from .views import get_weather
        mock_get_coordinates.return_value = (48.86, 2.3399997)
        mock_get.return_value.json.return_value = {
            'current': {
                'temperature_2m': 20,
                'precipitation': 0,
                'wind_speed_10m': 5,
                'relative_humidity_2m': 50
            }
        }
        weather = get_weather('Париж')
        print(weather)
        self.assertIn('temperature_2m', weather['current'])
        self.assertEqual(weather['current']['temperature_2m'], 20)
