from datetime import date

from apps.user.models import User


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
