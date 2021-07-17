from datetime import time
from django.db import models
from apps.common.models import BaseModel
from apps.user.models import User


class Sleep(BaseModel):
    owner: User = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    slept_date = models.DateField(auto_now_add=True)
    slept_time: time = models.TimeField(null=False)
    is_enough_sleep = models.BooleanField(null=False)
    used_phone_30_mins_before_sleep = models.BooleanField(null=False)
    tiredness_level = models.PositiveSmallIntegerField(
        null=False)  # should be between 1 and 5