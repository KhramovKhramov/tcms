from rest_framework import viewsets

from apps.user.api.filters import UserFilter
from apps.user.api.serializers import UserSerializer
from apps.user.models import User


class UserViewSet(viewsets.ModelViewSet):
    """API для работы с пользователями."""

    queryset = User.objects.all().order_by('-id')
    serializer_class = UserSerializer
    filterset_class = UserFilter
    http_method_names = ['get', 'post', 'patch', 'delete']
