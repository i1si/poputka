from rest_framework import serializers
from .models import City, Ride, Feedback
from users.models import User


class DriverSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'first_name', 'avatar',  'rating']


class RideSerializer(serializers.HyperlinkedModelSerializer):
    # ride_date = serializers.DateTimeField(source='ride_datetime', format='%Y-%m-%d')
    ride_datetime = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")
    driver = DriverSerializer(read_only=True)

    class Meta:
        model = Ride
        fields = ('driver', 'id', 'from_place', 'to_place', 'text', 'ride_datetime', 'seats_count', 'price')


class CitySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = City
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.DateTimeField(format='%d.%m.%Y', read_only=True)
    age = serializers.IntegerField()

    class Meta:
        model = User
        fields = ('first_name', 'date_joined', 'birthday', 'age', 'avatar', 'rating', 'ride_count', )
        read_only_fields = ('rating', 'ride_count', 'age', )


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
        fields = ('author', 'rating', 'date', 'text', )
