from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import F, Func
from django.db.models.functions import ExtractYear
from rest_framework import viewsets
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet

from .forms import AddRide, SearchRide
from .models import Ride, City, Feedback
from users.models import User
from .serializers import CitySerializer, RideSerializer, UserSerializer, FeedbackSerializer



def index(request):
    return render(request, 'main/index.html')


def search(request):
    form = SearchRide(request.GET) if SearchRide(request.GET).is_valid() else None
    return render(request, 'main/search.html', {'form': form})


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


# API
class RideViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows ...
    """
    serializer_class = RideSerializer    

    def get_queryset(self):
        """
        Restricts the returned rides, by filtering against a `from`, `to`,  `date`, `persons` query parameters in the URL.
        """
        from_place = self.request.query_params.get('from', None)
        to_place = self.request.query_params.get('to', None)
        ride_date = self.request.query_params.get('date', None)
        person_count = self.request.query_params.get('persons', None)
        if from_place and to_place and ride_date and person_count:
            queryset = Ride.objects.filter(from_place=from_place, to_place=to_place, ride_datetime__date=ride_date, 
                                        seats_count__gte=person_count)
            return queryset


class CityViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CitySerializer

    def get_queryset(self):
        user_query = self.request.query_params.get('q', None)
        if user_query:
            queryset = City.objects.filter(name__icontains=user_query)
            return queryset


class UserInfoView(RetrieveModelMixin, GenericViewSet):
    queryset = User.objects.annotate(
        age=ExtractYear(Func(F('birthday'), function='age'))
    )
    serializer_class = UserSerializer
    lookup_field = 'id'


class FeedbackViewSet(ListModelMixin, GenericViewSet):
    serializer_class = FeedbackSerializer

    def get_queryset(self):
        uid = self.request.query_params.get('uid', None)
        if uid:
            queryset = Feedback.objects.filter(rated_user=uid)
            return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        response = super().list(request, args, kwargs)
        rating_counts = {
            '1': queryset.filter(rating=1).count(),
            '2': queryset.filter(rating=2).count(),
            '3': queryset.filter(rating=3).count(),
            '4': queryset.filter(rating=4).count(),
            '5': queryset.filter(rating=5).count(),
            'total': queryset.count()
        }
        new_data = {
            'rating_counts': rating_counts,
            'feedbacks': response.data,
        }
        response.data = new_data
        return response

