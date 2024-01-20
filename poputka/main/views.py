from django.shortcuts import redirect, render


def index(request):
    return render(request, 'main/index.html')


def search(request):
    return render(request, 'main/search.html')


def offer(request):
    if request.user.is_authenticated:
        return render(request, 'main/offer.html')
    return redirect('login')
