from datetime import date

from apps.user.models import Athlete

from tests.factories import AthleteFactory, UserFactory
from tests.factories.group import GroupFactory
from tests.helpers.user import serialize_user


def create_athlete_request_data() -> dict:
    """
    Получение словаря с данными, необходимыми для
    создания спортсмена вместе с новым пользователем.
    """

    user = UserFactory.build()
    athlete = AthleteFactory.build()

    return {
        'user_data': {
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'date_of_birth': user.date_of_birth,
            'gender': user.gender,
            'phone': user.phone,
        },
        'playing_level': athlete.playing_level,
    }


def create_athletes_filtering_test_data() -> list[Athlete]:
    """
    Получение тестовых данных
    для проверки фильтрации и сортировки списка спортсменов.
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

    # Создание группы для тестирования фильтрации по группам
    group = GroupFactory.create(id=99)

    # Создаем и возвращаем спортсменов для тестов
    athletes = [
        AthleteFactory.create(
            user=user,
        )
        for user in users
    ]
    athletes[0].groups.add(group)

    return athletes


def serialize_athlete(athlete: Athlete) -> dict:
    """Сериализация модели спортсмена для использования в тестах."""

    return {
        'id': athlete.pk,
        'user': serialize_user(athlete.user),
        'date_from': athlete.date_from.strftime('%Y-%m-%d')
        if isinstance(athlete.date_from, date)
        else athlete.date_from,
        'date_to': athlete.date_to.strftime('%Y-%m-%d')
        if isinstance(athlete.date_to, date)
        else athlete.date_to,
        'playing_level': athlete.playing_level,
    }
