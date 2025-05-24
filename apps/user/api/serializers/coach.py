from rest_framework import serializers

from apps.user.api.serializers.user import (
    UserCreateNestedSerializer,
    UserSerializer,
)
from apps.user.models import Coach


class CoachSerializer(serializers.ModelSerializer):
    """Сериализатор данных тренера."""

    user = UserSerializer(
        label='Пользователь',
        read_only=True,
    )

    class Meta:
        model = Coach
        fields = '__all__'


class AppointCoachSerializer(serializers.ModelSerializer):
    """Сериализатор назначения пользователя тренером."""

    class Meta:
        model = Coach
        fields = (
            'position',
            'judge_category',
            'education',
            'additional_info',
            'achievements',
        )
        extra_kwargs = {
            'position': {'write_only': True},
            'judge_category': {'write_only': True},
            'education': {'write_only': True},
            'additional_info': {'write_only': True},
            'achievements': {'write_only': True},
        }


class CoachCreateSerializer(serializers.ModelSerializer):
    """Сериализатор создания роли тренера вместе с пользователем."""

    user_data = UserCreateNestedSerializer(
        label='Данные пользователя',
        write_only=True,
    )

    class Meta:
        model = Coach
        fields = (
            'user_data',
            'position',
            'judge_category',
            'education',
            'additional_info',
            'achievements',
        )
        extra_kwargs = {
            'position': {'write_only': True},
            'judge_category': {'write_only': True},
            'education': {'write_only': True},
            'additional_info': {'write_only': True},
            'achievements': {'write_only': True},
        }
