from django.urls import path
from .views import login_view, logout_view, register_view, register_confirm


urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='loguot'),
    path('register/', register_view, name='register'),
    path('register/confirm/<token>', register_confirm, name='register_confirm'),
]
