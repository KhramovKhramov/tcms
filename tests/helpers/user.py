from datetime import date

from apps.user.models import User

from tests.factories import UserFactory


def create_user_request_data() -> dict:
    """
    Получение словаря с данными, необходимыми для
    создания пользователя.
    """

    instance = UserFactory.build()

    return {
        'email': instance.email,
        'password': 'password',
        'first_name': instance.first_name,
        'last_name': instance.last_name,
        'date_of_birth': instance.date_of_birth,
        'gender': instance.gender,
        'phone': instance.phone,
    }


def update_user_request_data() -> dict:
    """
    Получение словаря с данными, необходимыми для
    обновления данных пользователя.
    """

    update_fields = ['first_name', 'last_name']

    return {key: create_user_request_data()[key] for key in update_fields}


def serialize_user(user: User) -> dict:
    """Сериализация модели пользователя для использования в тестах."""

    return {
        'id': user.pk,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'patronymic': user.patronymic,
        'date_of_birth': user.date_of_birth.strftime('%Y-%m-%d')
        if isinstance(user.date_of_birth, date)
        else user.date_of_birth,
        'gender': user.gender,
        'phone': user.phone,
    }
