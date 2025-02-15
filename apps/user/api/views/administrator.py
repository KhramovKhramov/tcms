from rest_framework import mixins, viewsets

from apps.user.api.serializers import AdministratorSerializer
from apps.user.models import Administrator


class AdministratorViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """API для работы с администраторами."""

    queryset = (
        Administrator.objects.all().order_by('-id').select_related('user')
    )
    serializer_class = AdministratorSerializer
