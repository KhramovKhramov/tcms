import pytest
from apps.user.models import User
from apps.user.tests.factories import UserFactory
from rest_framework.reverse import reverse
from rest_framework.test import APIClient


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


@pytest.fixture
def unauthorized_client() -> APIClient:
    """Неавторизованный клиент для отправки запросов в тестах."""

    return APIClient()


@pytest.fixture
def authorized_client(test_user) -> APIClient:
    """
    Авторизованный клиент для отправки запросов в тестах.

    :param test_user: Тестовый пользователь.
    """

    client = APIClient()
    client.force_authenticate(user=test_user)

    return client


@pytest.fixture
def authorized_superuser_client(test_superuser) -> APIClient:
    """
    Авторизованный под аккаунтом суперюзера
    клиент для отправки запросов в тестах.

    :param test_superuser: Тестовый суперюзер.
    """

    client = APIClient()
    client.force_authenticate(user=test_superuser)

    return client


def get_api_url(basename, pk: int | None = None) -> str:
    """Получение url для запроса через APIClient."""

    # TODO добавить возможность создавать url для кастомных экшенов
    if pk is None:
        return reverse(f'{basename}-list')
    return reverse(f'{basename}-detail', kwargs={'pk': pk})
