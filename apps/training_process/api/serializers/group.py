from rest_framework import serializers

from apps.training_process.models import Group
from apps.user.api.serializers import CoachSerializer
from apps.user.models import Coach


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор данных группы."""

    coach_id = serializers.PrimaryKeyRelatedField(
        label='id тренера',
        queryset=Coach.objects.all(),
        source='coach',
        write_only=True,
    )
    coach = CoachSerializer(
        label='Тренер',
        read_only=True,
    )

    class Meta:
        model = Group
        fields = '__all__'
