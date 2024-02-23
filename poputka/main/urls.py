from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from rest_framework import routers
from .views import CityViewSet, index, search, offer, show_ride, RideViewSet, UserInfoView, FeedbackViewSet


router = routers.DefaultRouter()
router.register(r'rides', RideViewSet, basename='ride')
router.register(r'cities', CityViewSet, basename='city')
router.register(r'users', UserInfoView, basename='user')
router.register(r'feedbacks', FeedbackViewSet, basename='feedback')

urlpatterns = [
    path('', index, name='main'),
    path('search/', search, name='search'),
    path('offer/', offer, name='offer'),
    path('rides/<int:ride_id>/', show_ride, name='ride'),
    path('api/v1/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
