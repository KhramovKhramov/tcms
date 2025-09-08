import pytest

from tests.factories import AdministratorFactory


@pytest.mark.django_db
def test_administrator_full_name():
    """Проверка работы вычисляемого поля с ФИО администратора."""

    administrators = AdministratorFactory.create_batch(3)

    for administrator in administrators:
        full_name = (
            f'{administrator.user.last_name} '
            f'{administrator.user.first_name} '
            f'{administrator.user.patronymic or ""}'
        )

        assert administrator.user.full_name == full_name.strip()
