from django.shortcuts import render
from .forms import CityForm
from .models import CitySearchCount
from .utils import get_weather
from cities_light.models import City
import json
import uuid


def index(request):
    suggestions = []
    weather_data = None
    user = request.COOKIES.get('user', None)
    if not user:
        user = str(uuid.uuid4())
    search_history_cookie = json.loads(request.COOKIES.get('search_history', '[]'))

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            city_name = form.cleaned_data['city']

            suggestions = City.objects.filter(name__icontains=city_name).values_list('name', flat=True)[:5]
            weather_data = get_weather(city_name)

            if city_name not in [entry['city'] for entry in search_history_cookie]:
                search_history_cookie.append({'city': city_name})

            city_count, created = CitySearchCount.objects.get_or_create(city=city_name, user=user)
            if not created:
                city_count.count += 1
                city_count.save()

            response = render(request, 'index.html',
                              {'form': form, 'weather_data': weather_data, 'suggestions': suggestions,
                               'search_history': search_history_cookie})
            response.set_cookie('search_history', json.dumps(search_history_cookie), max_age=365 * 24 * 60 * 60)
            response.set_cookie('user', user, max_age=365 * 24 * 60 * 60)
            print(weather_data)
            return response
    else:
        form = CityForm()

    return render(request, 'index.html',
                  {'form': form, 'weather_data': weather_data, 'suggestions': suggestions,
                   'search_history': search_history_cookie})


def history(request):
    user = request.COOKIES.get('user', None)
    search_history_cookie = json.loads(request.COOKIES.get('search_history', '[]'))
    city_counts = CitySearchCount.objects.filter(user=user)
    return render(request, 'history.html', {'searches': search_history_cookie, 'city_counts': city_counts})

