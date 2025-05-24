from rest_framework import serializers

from apps.user.api.serializers.user import (
    UserCreateNestedSerializer,
    UserSerializer,
)
from apps.user.models import Athlete


class AthleteSerializer(serializers.ModelSerializer):
    """Сериализатор данных спортсмена."""

    user = UserSerializer(
        label='Пользователь',
        read_only=True,
    )

    class Meta:
        model = Athlete
        # TODO возможно, стоит добавить группы для retrieve()
        fields = (
            'id',
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


class AthleteCreateSerializer(serializers.ModelSerializer):
    """Сериализатор создания роли спортсмена вместе с пользователем."""

    user_data = UserCreateNestedSerializer(
        label='Данные пользователя',
        write_only=True,
    )

    class Meta:
        model = Athlete
        fields = ('user_data', 'playing_level')
        extra_kwargs = {
            'playing_level': {'write_only': True},
        }
