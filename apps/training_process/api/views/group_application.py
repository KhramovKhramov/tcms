from rest_framework import viewsets

from apps.training_process.api.serializers import GroupApplicationSerializer
from apps.training_process.models import GroupApplication


class GroupApplicationViewSet(viewsets.ModelViewSet):
    """API для работы с тренировочными группами."""

    queryset = (
        GroupApplication.objects.all()
        .select_related('group__coach__user', 'user')
        .order_by('-id')
    )
    serializer_class = GroupApplicationSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

    # TODO редактировать/удалять заявки можно только в статусе Новая
