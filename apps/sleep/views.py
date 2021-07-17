from datetime import datetime
from drf_spectacular.utils import extend_schema
from django.http.request import HttpRequest
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.user.models import User
from apps.sleep.models import Sleep
from apps.sleep.permissions import IsOwner
from apps.sleep.serializers import SleepSerializer


class SleepView(mixins.CreateModelMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = SleepSerializer
    permission_classes = (IsOwner, )

    def perform_create(self, serializer: SleepSerializer):
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return Sleep.objects.filter(
            owner=self.request.user).order_by('-slept_date')

    @action(methods=['get'], detail=False)
    def today(self, request: HttpRequest, *args, **kwargs):
        user: User = self.request.user
        today_sleep = Sleep.objects.filter(owner=user,
                                           slept_date=datetime.today().date())
        if today_sleep.exists():
            serializer: SleepSerializer = self.get_serializer(
                today_sleep.first())
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
