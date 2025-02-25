from rest_framework import serializers

from apps.user.api.serializers import UserSerializer
from apps.user.models import Athlete, User


class AthleteSerializer(serializers.ModelSerializer):
    """Сериализатор данных спортсмена."""

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
        model = Athlete
        fields = '__all__'
