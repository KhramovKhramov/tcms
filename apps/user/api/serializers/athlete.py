from rest_framework import serializers

from apps.user.api.serializers.user import UserSerializer
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
        # TODO возможно, стоит добавить группы для retrieve()
        fields = (
            'id',
            'user_id',
            'user',
            'date_from',
            'date_to',
            'playing_level',
        )


class AppointAthleteSerializer(serializers.ModelSerializer):
    """Сериализатор назначения пользователя спортсменом."""

    class Meta:
        model = Athlete
        fields = ('playing_level',)
        extra_kwargs = {
            'playing_level': {'write_only': True},
        }
