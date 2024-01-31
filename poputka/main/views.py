from django.shortcuts import get_object_or_404, redirect, render
from .forms import AddRide, SearchRide
from .models import Ride


def index(request):
    return render(request, 'main/index.html')


def search(request):
    form = SearchRide(request.GET)
    if form.is_valid():
        from_place = request.GET.get('from_place')
        to_place = request.GET.get('to_place')
        ride_date = request.GET.get('ride_date')
        person_count = request.GET.get('person_count')
        rides = Ride.objects.filter(from_place=from_place, to_place=to_place, ride_datetime__date=ride_date, 
                                    seats_count__gte=person_count)
    else:
        form = SearchRide()
        rides = None
    return render(request, 'main/search.html', {'form': form, 'rides': rides})


def offer(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        form = AddRide(request.POST)
        if form.is_valid():
            ride = Ride(**form.cleaned_data, driver_id=request.user.id)
            ride.save()
            return redirect('ride', ride_id=ride.id)
    else:
        form = AddRide()
    return render(request, 'main/offer.html', {'form': form})


def show_ride(request, ride_id):
    ride = get_object_or_404(Ride, id=ride_id)
    return render(request, 'main/ride.html', {'ride': ride})
