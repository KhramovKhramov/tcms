from datetime import date

from apps.user.models import Coach
from apps.user.models.choices import CoachPosition

from tests.factories import CoachFactory, UserFactory
from tests.helpers.user import serialize_user


def create_coach_request_data() -> dict:
    """
    Получение словаря с данными, необходимыми для
    создания тренера вместе с новым пользователем.
    """

    user = UserFactory.build()
    coach = CoachFactory.build()

    return {
        'user_data': {
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'date_of_birth': user.date_of_birth,
            'gender': user.gender,
            'phone': user.phone,
        },
        'position': coach.position,
        'coach_experience': coach.coach_experience,
    }


def create_coaches_filtering_test_data() -> list[Coach]:
    """
    Получение тестовых данных
    для проверки фильтрации и сортировки списка тренеров.
    """

    # Данные пользователей
    user_data = [
        {
            'last_name': 'Суплотова',
            'first_name': 'Людмила',
            'patronymic': 'Александровна',
        },
        {
            'last_name': 'Брельгин',
            'first_name': 'Макар',
            'patronymic': 'Игоревич',
        },
        {
            'last_name': 'Большакова',
            'first_name': 'Кристина',
            'patronymic': 'Сергеевна',
        },
    ]

    # Создание пользователей
    users = [UserFactory.create(**data) for data in user_data]

    # Создаем и возвращаем тренеров для тестов
    return [
        CoachFactory.create(
            user=users[0],
            position=CoachPosition.INSTRUCTOR,
            coach_experience=5,
        ),
        CoachFactory.create(
            user=users[1],
            position=CoachPosition.INSTRUCTOR,
            coach_experience=3,
        ),
        CoachFactory.create(
            user=users[2],
            position=CoachPosition.SENIOR,
            coach_experience=8,
        ),
    ]


def serialize_coach(coach: Coach) -> dict:
    """Сериализация модели тренера для использования в тестах."""

    return {
        'id': coach.pk,
        'user': serialize_user(coach.user),
        'date_from': coach.date_from.strftime('%Y-%m-%d')
        if isinstance(coach.date_from, date)
        else coach.date_from,
        'date_to': coach.date_to.strftime('%Y-%m-%d')
        if isinstance(coach.date_to, date)
        else coach.date_to,
        'position': coach.position,
        'current_coach_experience': coach.current_coach_experience,
        'judge_category': coach.judge_category,
        'education': coach.education,
        'additional_info': coach.additional_info,
        'achievements': coach.achievements,
    }
