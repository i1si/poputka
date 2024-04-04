from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from rest_framework import routers
import main.views as v


router = routers.DefaultRouter()
router.register(r'rides', v.RideViewSet, basename='ride')
router.register(r'cities', v.CityViewSet, basename='city')
router.register(r'users', v.UserInfoView, basename='user')
router.register(r'feedbacks', v.FeedbackViewSet, basename='feedback')

urlpatterns = [
    path('', v.index, name='main'),
    path('search/', v.search, name='search'),
    path('offer/', v.offer, name='offer'),
    path('rides/<int:ride_id>/', v.show_ride, name='ride'),
    path('myrides/', v.show_user_rides, name='user_rides'),
    path('api/v1/', include(router.urls)),
    path('api/v1/book/', v.book_ride),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
