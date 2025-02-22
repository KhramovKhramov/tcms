from datetime import date

from apps.user.models import Coach, User


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
        'judge_category': coach.judge_category,
        'education': coach.education,
        'additional_info': coach.additional_info,
        'achievements': coach.achievements,
    }
