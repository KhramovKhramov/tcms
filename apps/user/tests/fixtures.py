import pytest

from apps.user.models import User
from apps.user.tests.factories import UserFactory


@pytest.fixture
def test_user() -> User:
    """Фикстура, возвращающая тестового пользователя."""

    return UserFactory.create(
        is_superuser=False,
    )


@pytest.fixture
def test_superuser() -> User:
    """Фикстура, возвращающая тестового суперюзера."""

    return UserFactory.create(
        is_superuser=True,
    )
