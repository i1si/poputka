from rest_framework import serializers
from .models import City, Ride
from users.models import User


class DriverSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'avatar',  'rating']


class RideSerializer(serializers.HyperlinkedModelSerializer):
    ride_time = serializers.DateTimeField(source="ride_datetime", format="%H:%M")
    driver = DriverSerializer()
    
    class Meta:
        model = Ride
        fields = ['id', 'from_place', 'to_place', 'ride_time', 'seats_count', 'driver', 'price']


class CitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = City
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    last_login = serializers.DateTimeField(format='%d.%m.%Y')
    date_joined = serializers.DateTimeField(format='%d.%m.%Y')
    age = serializers.IntegerField()

    class Meta:
        model = User
        depth = 1
        fields = ('first_name', 'last_login', 'date_joined', 'age', 'avatar', 'rating', 'ride_count')
