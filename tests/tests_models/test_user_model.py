import pytest

from tests.factories import UserFactory


@pytest.mark.django_db
def test_user_full_name():
    """Проверка работы вычисляемого поля с ФИО пользователя."""

    users = UserFactory.create_batch(2)
    another_user = UserFactory.create(
        patronymic='Ивановна',
    )

    for user in [*users, another_user]:
        full_name = (
            f'{user.last_name} {user.first_name} {user.patronymic or ""}'
        )

        assert user.full_name == full_name.strip()
