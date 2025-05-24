from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from apps.user.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор данных пользователя."""

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'password',
            'first_name',
            'last_name',
            'patronymic',
            'date_of_birth',
            'gender',
            'phone',
        )
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def save(self, **kwargs):
        password = self.validated_data.get('password')
        # TODO унифицировать создание пароля
        if password:
            self.validated_data['password'] = make_password(password)

        return super().save(**kwargs)


class UserCreateNestedSerializer(serializers.ModelSerializer):
    """
    Вложенный сериализатор данных пользователя
    при создании пользователя вместе с ролью.
    """

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'patronymic',
            'date_of_birth',
            'gender',
            'phone',
        )
        extra_kwargs = {
            'email': {'write_only': True},
            'first_name': {'write_only': True},
            'last_name': {'write_only': True},
            'patronymic': {'write_only': True},
            'date_of_birth': {'write_only': True},
            'gender': {'write_only': True},
            'phone': {'write_only': True},
        }
