from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from apps.person.models import Person


class PersonSerializer(serializers.ModelSerializer):
    """Сериализатор данных пользователя."""

    class Meta:
        model = Person
        fields = (
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
        if password:
            self.validated_data['password'] = make_password(password)

        return super().save(**kwargs)