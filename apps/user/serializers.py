from datetime import time
from rest_framework import serializers
from apps.user.validators import validate_hour_minute_format
from apps.user.models import User


class UserSerializer(serializers.ModelSerializer):
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

    class Meta:
        model = User
        fields = ('username', 'password', 'name', 'weight_kg',
                  'average_sleep_time', 'bedtime_starts_at', 'date_joined')
