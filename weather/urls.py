from django.urls import path
from .views import index, history, autocomplete

urlpatterns = [
    path('', index, name='index'),
    path('history/', history, name='history'),
    path('autocomplete/', autocomplete, name='autocomplete'),
]
