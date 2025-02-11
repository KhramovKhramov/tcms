import pytest

from apps.user.tests.factories import UserFactory


class TestUserModel:
    """Тесты модели пользователя."""

    @pytest.mark.django_db
    def test_full_name(self):
        """Проверка работы вычисляемого поля с ФИО пользователя."""

        users = UserFactory.create_batch(2)
        another_user = UserFactory.create(
            patronymic='Ивановна',
        )

        for user in [*users, another_user]:
            full_name = (
                f'{user.last_name} {user.first_name} '
                f'{user.patronymic or ""}'
            )

            assert user.full_name == full_name.strip()
