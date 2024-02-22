from rest_framework import serializers
from .models import City, Ride, Feedback
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
    date_joined = serializers.DateTimeField(format='%d.%m.%Y')
    age = serializers.IntegerField()

    class Meta:
        model = User
        depth = 1
        fields = ('first_name', 'date_joined', 'birthday', 'age', 'avatar', 'rating', 'ride_count')


class AuthorSerializer(serializers.ModelSerializer):
    uri = serializers.URLField(read_only=True, source='get_url_path')

    class Meta:
        model = User
        fields = ('id', 'uri', 'first_name', 'avatar')


class FeedbackSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    rating = serializers.CharField(source='get_rating_display')
    date = serializers.DateField(format='%d.%m.%Y')

    class Meta:
        model = Feedback
        fields = ('author', 'rating', 'date', 'text',)
