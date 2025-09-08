from datetime import date

from apps.user.models import Administrator

from tests.factories import AdministratorFactory, UserFactory
from tests.helpers.user import serialize_user


def create_administrator_request_data() -> dict:
    """
    Получение словаря с данными, необходимыми для
    создания администратора вместе с новым пользователем.
    """

    instance = UserFactory.build()

    return {
        'user_data': {
            'email': instance.email,
            'first_name': instance.first_name,
            'last_name': instance.last_name,
            'date_of_birth': instance.date_of_birth,
            'gender': instance.gender,
            'phone': instance.phone,
        }
    }


def create_administrators_filtering_test_data() -> list[Administrator]:
    """
    Получение тестовых данных
    для проверки фильтрации и сортировки списка администраторов.
    """

    # Данные пользователей
    user_data = [
        {
            'last_name': 'Кривоногова',
            'first_name': 'Алевтина',
            'patronymic': 'Васильевна',
        },
        {
            'last_name': 'Иванов',
            'first_name': 'Иван',
            'patronymic': 'Иванович',
        },
        {
            'last_name': 'Большакова',
            'first_name': 'Кристина',
            'patronymic': 'Сергеевна',
        },
    ]

    # Создание пользователей
    users = [UserFactory.create(**data) for data in user_data]

    # Создаем и возвращаем администраторов для тестов
    return [
        AdministratorFactory.create(
            user=user,
        )
        for user in users
    ]


def serialize_administrator(administrator: Administrator) -> dict:
    """Сериализация модели администратора для использования в тестах."""

    return {
        'id': administrator.pk,
        'user': serialize_user(administrator.user),
        'date_from': administrator.date_from.strftime('%Y-%m-%d')
        if isinstance(administrator.date_from, date)
        else administrator.date_from,
        'date_to': administrator.date_to.strftime('%Y-%m-%d')
        if isinstance(administrator.date_to, date)
        else administrator.date_to,
    }
