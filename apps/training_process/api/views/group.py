from rest_framework import mixins, viewsets

from apps.training_process.api.serializers import GroupSerializer
from apps.training_process.models import Group


class GroupViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    """API для работы с тренировочными группами."""

    queryset = (
        Group.objects.all().select_related('coach__user').order_by('-id')
    )
    serializer_class = GroupSerializer
    http_method_names = ['get', 'post', 'patch']
