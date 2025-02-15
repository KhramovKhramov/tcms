from rest_framework import serializers

from apps.user.api.serializers.user import UserSerializer
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
