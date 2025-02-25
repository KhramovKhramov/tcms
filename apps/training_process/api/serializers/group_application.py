from rest_framework import serializers

from apps.training_process.api.serializers.group import GroupSerializer
from apps.training_process.models import Group
from apps.training_process.models.group_application import GroupApplication
from apps.user.api.serializers import UserSerializer
from apps.user.models import User


class GroupApplicationSerializer(serializers.ModelSerializer):
    """Сериализатор данных заявки на присоединение к группе."""

    user_id = serializers.PrimaryKeyRelatedField(
        label='id пользователя',
        queryset=User.objects.all(),
        source='user',
        write_only=True,
    )
    user = UserSerializer(
        label='Пользователь',
        read_only=True,
    )

    group_id = serializers.PrimaryKeyRelatedField(
        label='id группы',
        queryset=Group.objects.all(),
        source='group',
        write_only=True,
    )
    group = GroupSerializer(
        label='Группа',
        read_only=True,
    )

    class Meta:
        model = GroupApplication
        fields = '__all__'
