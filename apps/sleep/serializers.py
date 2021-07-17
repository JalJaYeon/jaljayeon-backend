from datetime import time, datetime
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from apps.user.models import User
from apps.sleep.models import Sleep


class SleepSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(read_only=True)
    slept_date: datetime = serializers.DateField(read_only=True)
    slept_time: time = serializers.TimeField(format="%H:%M", required=True)
    is_enough_sleep = serializers.BooleanField(required=True)
    used_phone_30_mins_before_sleep = serializers.BooleanField(required=True)
    tiredness_level = serializers.IntegerField(min_value=1,
                                               max_value=5,
                                               required=True)
    ai_advice: str = serializers.SerializerMethodField()

    def get_ai_advice(self, obj: Sleep):
        if obj.tiredness_level > 3:
            return "- 수면 시간을 7시간으로 늘리세요\n- 취침 전 휴대폰 사용은 좋지 않아요"
        return "좋은 수면을 하셨습니다. 앞으로 유지해주세요"

    def validate(self, attrs):
        user: User = self.context['request'].user
        if Sleep.objects.filter(owner=user,
                                slept_date=datetime.today().date()).exists():
            raise ValidationError("You can upload one sleep report per day")
        return attrs

    class Meta:
        model = Sleep
        fields = ('id', 'owner', 'slept_date', 'slept_time', 'is_enough_sleep',
                  'used_phone_30_mins_before_sleep', 'tiredness_level',
                  'ai_advice')
