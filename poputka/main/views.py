from django.shortcuts import render


def index(request):
    return render(request, 'main/index.html')


def search(request):
    return render(request, 'main/search.html')


def offer(request):
    return render(request, 'main/offer.html')
