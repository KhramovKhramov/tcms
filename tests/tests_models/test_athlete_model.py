import pytest

from tests.factories import AthleteFactory


@pytest.mark.django_db
def test_athlete_full_name():
    """Проверка работы вычисляемого поля с ФИО спортсмена."""

    athletes = AthleteFactory.create_batch(3)

    for athlete in athletes:
        full_name = (
            f'{athlete.user.last_name} '
            f'{athlete.user.first_name} '
            f'{athlete.user.patronymic or ""}'
        )

        assert athlete.user.full_name == full_name.strip()
