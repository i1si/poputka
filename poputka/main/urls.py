from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import index, search, offer, show_ride


urlpatterns = [
    path('', index, name='main'),
    path('search/', search, name='search'),
    path('offer/', offer, name='offer'),
    path('ride/<int:ride_id>/', show_ride, name='ride'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
