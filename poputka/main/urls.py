from django.urls import path
from .views import index, search, offer


urlpatterns = [
    path('', index, name='main'),
    path('search/', search, name='search'),
    path('offer/', offer, name='offer'),
]
