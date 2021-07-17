import typing
from datetime import time
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from apps.user.validators import validate_hour_minute_format
from apps.user.models import User


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=(UniqueValidator(queryset=User.objects.all()), ), )
    password = serializers.CharField(write_only=True, required=True)
    average_sleep_time = serializers.CharField(
        min_length=5,
        max_length=5,
        required=True,
        validators=[validate_hour_minute_format])
    bedtime_starts_at = serializers.CharField(
        min_length=5,
        max_length=5,
        required=True,
        validators=[validate_hour_minute_format])

    average_sleep_time: time = serializers.TimeField(format="%H:%M")
    bedtime_starts_at: time = serializers.TimeField(format="%H:%M")

    def create(self, data: typing.Dict):
        user = User.objects.create(
            username=data["username"],
            name=data["name"],
            weight_kg=data["weight_kg"],
            average_sleep_time=data["average_sleep_time"],
            bedtime_starts_at=data["bedtime_starts_at"],
        )
        user.set_password(data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ('username', 'password', 'name', 'weight_kg',
                  'average_sleep_time', 'bedtime_starts_at', 'date_joined')
