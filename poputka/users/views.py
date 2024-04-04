from uuid import uuid4
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.core.cache import cache
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy

from .models import User
from main.models import Feedback
from .tasks import send_email
from .forms import AuthForm, RegisterForm


def login_view(request):
    if request.method == 'POST':
        auth_form = AuthForm(request.POST)
        if auth_form.is_valid():
            email = auth_form.cleaned_data['email']
            password = auth_form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return redirect('main')
                else:
                    auth_form.add_error('__all__', 'Данная учетная запись не активна')
            else:
                auth_form.add_error('__all__', 'Неправильный логин или пароль')
    elif request.user.is_authenticated:
        return redirect('main')
    else:
        auth_form = AuthForm()
    return render(request, 'users/login.html', context={'form': auth_form})


def logout_view(request):
    logout(request)
    return redirect('main')


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            token = uuid4().hex
            redis_key = settings.DJ_USER_CONFIRMATION_KEY.format(token=token)
            cache.set(redis_key, email, timeout=settings.DJ_USER_CONFIRMATION_TIMEOUT)
            confirmation_link = request.build_absolute_uri(
                reverse_lazy('register_confirm', kwargs={'token': token})
            )
            send_email.delay(
                'Попутка - Подтвердите свою почту',
                f'Для подтверждения почты перейдите по ссылке:\n\n{confirmation_link}',
                [email,]
            )
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            return render(request, 'users/register_confirm.html', context={'email': email})
    elif request.user.is_authenticated:
        return redirect('main')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', context={'form': form})


def register_confirm(request, token):
    redis_key = settings.DJ_USER_CONFIRMATION_KEY.format(token=token)
    user_email = cache.get(redis_key) or {}
    if user_email:
        user = User.objects.get(email=user_email)
        user.is_verified = True
        user.save()
        return render(request, 'users/register_confirmed.html')
    return redirect('main')


def profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    feedback_list = Feedback.objects.filter(rated_user=user)
    is_owner = request.user.id == user.id
    return render(request, 'users/profile.html', context={'user': user, 'feedback_list': feedback_list, 'is_owner': is_owner})


def edit_profile(request, user_id): 
    if request.user.id != user_id:
        raise Http404('The link seems to be broken :(')
    return render(request, 'users/edit_profile.html')
