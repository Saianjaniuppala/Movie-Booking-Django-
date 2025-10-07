from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Movie, Show, Booking


User = get_user_model()


class SignupSerializer(serializers.ModelSerializer):
password = serializers.CharField(write_only=True)
class Meta:
model = User
fields = ('id', 'username', 'email', 'password')


def create(self, validated_data):
user = User.objects.create_user(
username=validated_data['username'],
email=validated_data.get('email'),
password=validated_data['password']
)
return user


class MovieSerializer(serializers.ModelSerializer):
class Meta:
model = Movie
fields = ('id', 'title', 'duration_minutes')


class ShowSerializer(serializers.ModelSerializer):
movie = MovieSerializer(read_only=True)
class Meta:
model = Show
fields = ('id', 'movie', 'screen_name', 'date_time', 'total_seats')


class BookingSerializer(serializers.ModelSerializer):
show = ShowSerializer(read_only=True)
class Meta:
model = Booking
fields = ('id', 'user', 'show', 'seat_number', 'status', 'created_at')
read_only_fields = ('user', 'status', 'created_at')


class CreateBookingSerializer(serializers.Serializer):
seat_number = serializers.IntegerField(min_value=1)


def validate_seat_number(self, value):
show = self.context.get('show')
if not show:
raise serializers.ValidationError('Show context not provided')
if value > show.total_seats:
raise serializers.ValidationError('seat_number exceeds total seats for this show')
return value
