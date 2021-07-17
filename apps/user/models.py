from datetime import time
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self,
                    username,
                    name,
                    weight_kg,
                    average_sleep_time,
                    bedtime_starts_at,
                    password=None):
        user = self.model(
            username=username,
            name=name,
            weight_kg=weight_kg,
            average_sleep_time=average_sleep_time,
            bedtime_starts_at=bedtime_starts_at,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, name, password):
        user = self.create_user(
            username=username,
            name=name,
            password=password,
            # set unneccessary fields for superuser
            weight_kg=0,
            average_sleep_time=time(00, 00),
            bedtime_starts_at=time(00, 00),
        )
        user.is_superuser = True
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=
        _('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'
          ),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    name = models.CharField(max_length=10, null=False, blank=False)
    weight_kg = models.PositiveSmallIntegerField(null=False)

    average_sleep_time = models.TimeField(null=False)
    bedtime_starts_at = models.TimeField(null=False)

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name']

    class Meta:
        db_table = "jaljayeon_backend_user"