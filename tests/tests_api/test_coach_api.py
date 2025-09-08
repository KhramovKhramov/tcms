import pytest
from apps.user.models import Coach
from configs import settings
from django.utils.timezone import now
from rest_framework import status

from tests.conftest import check_filters_and_ordering
from tests.factories import CoachFactory
from tests.helpers import (
    create_coach_request_data,
    create_coaches_filtering_test_data,
    serialize_coach,
)
from tests.utils import get_api_url


@pytest.mark.django_db
def test_coach_create(authorized_client, coach_list_url):
    """Тест создания тренера вместе с пользователем."""

    response = authorized_client.post(
        coach_list_url,
        data=create_coach_request_data(),
        format='json',
    )
    assert response.status_code == status.HTTP_201_CREATED

    instance = Coach.objects.get(pk=response.data['id'])
    assert response.data == serialize_coach(instance)


@pytest.mark.django_db
def test_coach_retrieve(authorized_client, coach):
    """Тест получения данных тренера по идентификатору."""

    response = authorized_client.get(
        get_api_url('coaches', 'detail', pk=coach.pk)
    )
    assert response.status_code == status.HTTP_200_OK

    assert response.data == serialize_coach(coach)


@pytest.mark.django_db
def test_coaches_list(authorized_client, coach_list_url, coaches):
    """Тест получения списка тренеров."""

    response = authorized_client.get(coach_list_url)
    assert response.status_code == status.HTTP_200_OK

    assert response.data['results'][0] == serialize_coach(coaches[-1])


@pytest.mark.django_db
def test_coaches_list_pagination(authorized_client, coach_list_url):
    """Тест пагинации в списке тренеров."""

    CoachFactory.create_batch(30)

    response = authorized_client.get(coach_list_url)
    assert response.status_code == status.HTTP_200_OK

    page_size = settings.REST_FRAMEWORK['PAGE_SIZE']
    assert len(response.data['results']) == page_size


@pytest.mark.django_db
def test_coaches_list_max_queries(
    authorized_client,
    coach_list_url,
    coaches,
    django_assert_max_num_queries,
):
    """
    Тест проверки максимального количество запросов
    в списке тренеров.
    """

    # Количество записей для пагинации
    # Основной запрос
    with django_assert_max_num_queries(2):
        response = authorized_client.get(coach_list_url)
        assert response.status_code == status.HTTP_200_OK


# Остальные тесты API


@pytest.mark.django_db
def test_cancel_coach(authorized_client, coach):
    """Тест окончания действия роли тренера."""

    # Запрос на окончание действия роли
    response = authorized_client.post(
        get_api_url('coaches', 'cancel-coach', pk=coach.pk)
    )
    assert response.status_code == status.HTTP_200_OK

    # Проверяем, что действие роли тренера окончено
    coach.refresh_from_db()
    assert coach.date_to == now().date()

    # Проверяем, что если роль тренера уже недействующая, нельзя
    # окончить действие снова
    response = authorized_client.post(
        get_api_url('coaches', 'cancel-coach', pk=coach.pk)
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data[0] == (
        'Роль данного тренера уже не является действующей'
    )


# Тесты фильтрации и сортировки


@pytest.mark.parametrize(
    ('filter_param', 'expected_objects'),
    [
        ({'full_name': 'ак'}, [2, 1]),
        ({'full_name': 'Макар'}, [1]),
    ],
)
@pytest.mark.django_db
def test_filters(
    authorized_client, coach_list_url, filter_param, expected_objects
):
    """Тесты фильтрации списка тренеров."""

    check_filters_and_ordering(
        coach_list_url,
        authorized_client,
        create_coaches_filtering_test_data(),
        filter_param,
        expected_objects,
    )


@pytest.mark.parametrize(
    ('ordering_param', 'expected_objects'),
    [
        ({'ordering': ''}, [2, 1, 0]),
        ({'ordering': 'full_name'}, [2, 1, 0]),
        ({'ordering': '-full_name'}, [0, 1, 2]),
        ({'ordering': 'position'}, [0, 1, 2]),
        ({'ordering': '-position'}, [2, 0, 1]),
        ({'ordering': 'all_coach_experience'}, [1, 0, 2]),
        ({'ordering': '-all_coach_experience'}, [2, 0, 1]),
    ],
)
@pytest.mark.django_db
def test_ordering(
    authorized_client,
    coach_list_url,
    ordering_param,
    expected_objects,
):
    """Тесты сортировки списка тренеров."""

    check_filters_and_ordering(
        coach_list_url,
        authorized_client,
        create_coaches_filtering_test_data(),
        ordering_param,
        expected_objects,
    )
