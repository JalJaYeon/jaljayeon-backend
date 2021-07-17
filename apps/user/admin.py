from django.contrib import admin
from apps.sleep.models import Sleep
from apps.user.models import User


class SleepInline(admin.StackedInline):
    model = Sleep


@admin.register(User)
class User(admin.ModelAdmin):
    inlines = [SleepInline]