from uuid import uuid4
from django.conf import settings
from django.shortcuts import redirect, render
from django.core.cache import cache
from django.urls import reverse_lazy
from users.models import User

from users.tasks import send_email
from .forms import AuthForm, RegisterForm
from django.contrib.auth import authenticate, login, logout


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
                    return redirect('/')
                else:
                    auth_form.add_error('__all__', 'Данная учетная запись не активна')
            else:
                auth_form.add_error('__all__', 'Неправильный логин или пароль')

    else:
        auth_form = AuthForm()
    return render(request, 'users/login.html', context={'form': auth_form})


def logout_view(request):
    logout(request)
    return redirect('/')


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
    return redirect('/')


