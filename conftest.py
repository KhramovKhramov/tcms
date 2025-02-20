import pytest
from apps.user.models import User
from apps.user.tests.factories import UserFactory
from rest_framework import status
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


def get_api_url(basename: str, url_path: str, pk: int | None = None) -> str:
    """Получение url для запроса через APIClient."""

    if pk is None:
        return reverse(f'{basename}-{url_path}')
    return reverse(f'{basename}-{url_path}', kwargs={'pk': pk})


def check_filters_and_ordering(
    url, authorized_client, data, params, expected_objects
) -> None:
    """
    Базовая функция для тестирования фильтрации и сортировки.

    :param url: Урл для отправки запроса.
    :param authorized_client: Клиент для отправки запроса.
    :param data: Подготовленные данные для тестирования.
    :param params: Параметры фильтрации/сортировки.
    :param expected_objects: Ожидаемые в результате объекты.
    """

    response = authorized_client.get(
        url,
        data=params,
    )
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()['results']

    actual_ids = [item['id'] for item in response_data]
    expected_ids = [data[i].pk for i in expected_objects]
    assert actual_ids == expected_ids
