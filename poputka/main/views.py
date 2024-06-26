from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import F, Func, Q
from django.db.models.functions import ExtractYear
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, ListModelMixin, CreateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .forms import SearchRide
from .models import Ride, City, Feedback
from users.models import User
from .serializers import CitySerializer, RideSerializer, UserSerializer, FeedbackSerializer
from .permissions import IsOwnerOrReadOnly


def index(request):
    return render(request, 'main/index.html')


def search(request):
    form = SearchRide(request.GET) if SearchRide(request.GET).is_valid() else None
    return render(request, 'main/search.html', {'form': form})


def offer(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'main/offer.html')


def show_ride(request, ride_id):
    ride = get_object_or_404(Ride, id=ride_id)
    is_booked = ride.companions.filter(id=request.user.id).exists()
    return render(request, 'main/ride.html', {'ride': ride, 'is_booked': is_booked})


def show_user_rides(request):
    return render(request, 'main/userrides.html')


# API
class RideViewSet(ListModelMixin, CreateModelMixin, RetrieveModelMixin, GenericViewSet):
    """
    API endpoint that allows to create and receive trips.

    * Only ride owner are able to access unsafe methods.
    * Safe methods are available to all users.
    """

    serializer_class = RideSerializer
    permission_classes = (IsOwnerOrReadOnly, )
    queryset = Ride.objects.all()

    def list(self, request, *args, **kwargs):
        """
        Restricts the returned rides, by filtering against a `from`, `to`,  `date`, `persons` and uid 
        query parameters in the URL.
        """

        from_place = self.request.query_params.get('from', None)
        to_place = self.request.query_params.get('to', None)
        ride_date = self.request.query_params.get('date', None)
        person_count = self.request.query_params.get('persons', None)
        if from_place and to_place and ride_date and person_count:
            queryset = Ride.objects.filter(from_place=from_place, to_place=to_place, ride_datetime__date=ride_date, 
                                        seats_count__gte=person_count).order_by('ride_datetime')
        elif user_id := self.request.query_params.get('uid', None):
            queryset = Ride.objects.filter(Q(companions=user_id) | Q(driver_id=user_id))
        else:
            queryset = None
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(driver=self.request.user)


class CityViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows to get cities full name.
    """

    serializer_class = CitySerializer

    def get_queryset(self):
        user_query = self.request.query_params.get('q', None)
        if user_query:
            queryset = City.objects.filter(name__icontains=user_query)
            return queryset


class UserInfoView(RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    """
    API endpoint that allows to recieve and update user data.

    * Only owner are able to access unsafe methods.
    * Safe methods are available to all users.
    """

    queryset = User.objects.annotate(
        age=ExtractYear(Func(F('birthday'), function='age'))
    )
    serializer_class = UserSerializer
    lookup_field = 'id'
    permission_classes = (IsOwnerOrReadOnly, )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def book_ride(request):
    """
    API endpoint that allows to book ride.

    * Only authenticated users can access this endpoint.
    """

    if 'rideID' in request.data:
        companion = request.user
        ride = get_object_or_404(Ride, id=request.data['rideID'])
        ride.companions.set([companion])
        ride.seats_count -= 1
        return Response({'success': True})
    return Response({'success': False, 'msg': 'rideID is required'})


class FeedbackViewSet(ListModelMixin, GenericViewSet):
    """
    API endpoint that allows to create and recieve user feedbacks.
    """

    serializer_class = FeedbackSerializer
    # permission_classes = (IsOwnerOrReadOnly, )  # TODO если буду добавлять миксины

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
    
