from rest_framework import serializers

from apps.user.api.serializers.user import (
    UserCreateNestedSerializer,
    UserSerializer,
)
from apps.user.models import Administrator, User


class AdministratorSerializer(serializers.ModelSerializer):
    """Сериализатор данных администратора."""

    user_id = serializers.PrimaryKeyRelatedField(
        label='Идентификатор пользователя',
        queryset=User.objects.all(),
        source='user',
        write_only=True,
    )
    user = UserSerializer(
        label='Пользователь',
        read_only=True,
    )

    class Meta:
        model = Administrator
        fields = '__all__'


class AdministratorCreateSerializer(serializers.Serializer):
    """Сериализатор создания роли администратора вместе с пользователем."""

    user_data = UserCreateNestedSerializer(
        label='Данные пользователя',
        write_only=True,
    )
