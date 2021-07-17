from apps.sleep.models import Sleep
from rest_framework import mixins, viewsets
from apps.sleep.permissions import IsOwner
from apps.sleep.serializers import SleepSerializer


class SleepView(mixins.CreateModelMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = SleepSerializer
    permission_classes = (IsOwner, )

    def perform_create(self, serializer: SleepSerializer):
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        if self.action == 'list':
            return Sleep.objects.filter(owner=self.request.user)
        return Sleep.objects.all()