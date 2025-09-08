import pytest
from dateutil.relativedelta import relativedelta
from django.utils.timezone import now

from tests.factories import CoachFactory


@pytest.mark.django_db
def test_coach_full_name():
    """Проверка работы вычисляемого поля с ФИО тренера."""

    coaches = CoachFactory.create_batch(3)

    for coach in coaches:
        full_name = (
            f'{coach.user.last_name} '
            f'{coach.user.first_name} '
            f'{coach.user.patronymic or ""}'
        )

        assert coach.user.full_name == full_name.strip()


@pytest.mark.django_db
def test_current_coach_experience():
    """Проверка работы вычисляемого поля с общим тренерским стажем."""

    coaches = CoachFactory.create_batch(3)
    today = now().date()

    for coach in coaches:
        delta = relativedelta(today, coach.date_from)
        assert (
            coach.current_coach_experience
            == delta.years + coach.coach_experience
        )
