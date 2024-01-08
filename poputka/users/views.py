from django.shortcuts import redirect, render
from .forms import AuthForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.core.mail import send_mail


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
            confirmation_url = ''
            send_mail(
                'Попутка - Подтвердите свою почту', 
                f'Для подтверждения почты перейдите по ссылке:\n\n{confirmation_url}', 
                None, 
                [email,]
            )
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})
