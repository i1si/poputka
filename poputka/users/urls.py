from django.urls import path
from .views import login_view, logout_view, register_view, register_confirm, profile, edit_profile


urlpatterns = [
    path('<int:user_id>/', profile, name='profile'),
    path('<int:user_id>/edit', edit_profile, name='edit_profile'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('register/confirm/<token>', register_confirm, name='register_confirm'),
]
