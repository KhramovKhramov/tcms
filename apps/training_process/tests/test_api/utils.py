from apps.training_process.models import Group
from apps.user.tests.test_api.utils import serialize_coach


def serialize_group(group: Group) -> dict:
    """Сериализация модели группы для использования в тестах."""

    return {
        'id': group.pk,
        'name': group.name,
        'description': group.description,
        'status': group.status,
        'coach': serialize_coach(group.coach),
        'min_participants': group.min_participants,
        'max_participants': group.max_participants,
        'playing_level': group.playing_level,
        'training_days': group.training_days,
        'training_time': group.training_time,
        'trainings_start_date': group.trainings_start_date.strftime(
            '%Y-%m-%d'
        ),
    }
