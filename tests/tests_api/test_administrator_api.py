import pytest
from apps.user.models import Administrator
from configs import settings
from django.utils.timezone import now
from rest_framework import status

from tests.conftest import check_filters_and_ordering
from tests.factories import AdministratorFactory
from tests.helpers import (
    create_administrator_request_data,
    create_administrators_filtering_test_data,
    serialize_administrator,
)
from tests.utils import get_api_url

# CRUD-тесты


@pytest.mark.django_db
def test_administrator_create(authorized_client, administrator_list_url):
    """Тест создания администратора вместе с пользователем."""

    response = authorized_client.post(
        administrator_list_url,
        data=create_administrator_request_data(),
        format='json',
    )
    assert response.status_code == status.HTTP_201_CREATED

    instance = Administrator.objects.get(pk=response.data['id'])
    assert response.data == serialize_administrator(instance)


@pytest.mark.django_db
def test_administrators_list(
    authorized_client, administrator_list_url, administrators
):
    """Тест получения списка администраторов."""

    response = authorized_client.get(administrator_list_url)
    assert response.status_code == status.HTTP_200_OK

    assert response.data['results'][0] == serialize_administrator(
        administrators[-1]
    )


@pytest.mark.django_db
def test_administrators_list_pagination(
    authorized_client, administrator_list_url
):
    """Тест пагинации в списке администраторов."""

    AdministratorFactory.create_batch(30)

    response = authorized_client.get(administrator_list_url)
    assert response.status_code == status.HTTP_200_OK

    page_size = settings.REST_FRAMEWORK['PAGE_SIZE']
    assert len(response.data['results']) == page_size


@pytest.mark.django_db
def test_administrators_list_max_queries(
    authorized_client,
    administrator_list_url,
    administrators,
    django_assert_max_num_queries,
):
    """
    Тест проверки максимального количество запросов
    в списке администраторов.
    """

    # Количество записей для пагинации
    # Основной запрос
    with django_assert_max_num_queries(2):
        response = authorized_client.get(administrator_list_url)
        assert response.status_code == status.HTTP_200_OK


# Остальные тесты API


@pytest.mark.django_db
def test_cancel_administrator(authorized_client, administrator):
    """Тест окончания действия роли администратора."""

    # Запрос на окончание действия роли
    response = authorized_client.post(
        get_api_url(
            'administrators', 'cancel-administrator', pk=administrator.pk
        )
    )
    assert response.status_code == status.HTTP_200_OK

    # Проверяем, что действие роли администратора окончено
    administrator.refresh_from_db()
    assert administrator.date_to == now().date()

    # Проверяем, что если роль администратора уже недействующая, нельзя
    # окончить действие снова
    response = authorized_client.post(
        get_api_url(
            'administrators', 'cancel-administrator', pk=administrator.pk
        )
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data[0] == (
        'Роль данного администратора уже не является действующей'
    )


# Тесты фильтрации и сортировки


@pytest.mark.parametrize(
    ('filter_param', 'expected_objects'),
    [
        ({'full_name': 'ив'}, [1, 0]),
        ({'full_name': 'Крис'}, [2]),
    ],
)
@pytest.mark.django_db
def test_filters(
    authorized_client, administrator_list_url, filter_param, expected_objects
):
    """Тесты фильтрации списка администраторов."""

    check_filters_and_ordering(
        administrator_list_url,
        authorized_client,
        create_administrators_filtering_test_data(),
        filter_param,
        expected_objects,
    )


@pytest.mark.parametrize(
    ('ordering_param', 'expected_objects'),
    [
        ({'ordering': ''}, [2, 1, 0]),
        ({'ordering': 'full_name'}, [2, 1, 0]),
        ({'ordering': '-full_name'}, [0, 1, 2]),
    ],
)
@pytest.mark.django_db
def test_ordering(
    authorized_client,
    administrator_list_url,
    ordering_param,
    expected_objects,
):
    """Тесты сортировки списка администраторов."""

    check_filters_and_ordering(
        administrator_list_url,
        authorized_client,
        create_administrators_filtering_test_data(),
        ordering_param,
        expected_objects,
    )
