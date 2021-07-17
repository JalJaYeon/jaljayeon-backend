from django.contrib import admin
from apps.sleep.models import Sleep


@admin.register(Sleep)
class Sleep(admin.ModelAdmin):
    list_display = ('id', 'owner', 'slept_date', 'slept_time',
                    'is_enough_sleep', 'used_phone_30_mins_before_sleep',
                    'tiredness_level')
    list_editable = list_display[1:]