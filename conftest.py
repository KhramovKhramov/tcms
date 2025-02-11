import pytest
from rest_framework.test import APIClient


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