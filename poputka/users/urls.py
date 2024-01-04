from django.urls import path
from users.views import login_view, logout_view, register_view


urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='loguot'),
    path('register/', register_view, name='register')
]