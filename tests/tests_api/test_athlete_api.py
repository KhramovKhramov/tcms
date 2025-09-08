import pytest
from apps.user.models import Athlete
from configs import settings
from django.utils.timezone import now
from rest_framework import status

from tests.conftest import check_filters_and_ordering
from tests.factories import AthleteFactory
from tests.helpers import (
    create_athlete_request_data,
    create_athletes_filtering_test_data,
    serialize_athlete,
)
from tests.utils import get_api_url

# CRUD-тесты


@pytest.mark.django_db
def test_athlete_create(authorized_client, athlete_list_url):
    """Тест создания спортсмена вместе с пользователем."""

    response = authorized_client.post(
        athlete_list_url,
        data=create_athlete_request_data(),
        format='json',
    )
    assert response.status_code == status.HTTP_201_CREATED

    instance = Athlete.objects.get(pk=response.data['id'])
    assert response.data == serialize_athlete(instance)


@pytest.mark.django_db
def test_athlete_retrieve(authorized_client, athlete):
    """Тест получения данных спортсмена по идентификатору."""

    response = authorized_client.get(
        get_api_url('athletes', 'detail', pk=athlete.pk)
    )
    assert response.status_code == status.HTTP_200_OK

    assert response.data == serialize_athlete(athlete)


@pytest.mark.django_db
def test_athletes_list(authorized_client, athlete_list_url, athletes):
    """Тест получения списка спортсменов."""

    response = authorized_client.get(athlete_list_url)
    assert response.status_code == status.HTTP_200_OK

    assert response.data['results'][0] == serialize_athlete(athletes[-1])


@pytest.mark.django_db
def test_athletes_list_pagination(authorized_client, athlete_list_url):
    """Тест пагинации в списке спортсменов."""

    AthleteFactory.create_batch(30)

    response = authorized_client.get(athlete_list_url)
    assert response.status_code == status.HTTP_200_OK

    page_size = settings.REST_FRAMEWORK['PAGE_SIZE']
    assert len(response.data['results']) == page_size


@pytest.mark.django_db
def test_athletes_list_max_queries(
    authorized_client,
    athlete_list_url,
    athletes,
    django_assert_max_num_queries,
):
    """
    Тест проверки максимального количество запросов
    в списке спортсменов.
    """

    # Количество записей для пагинации
    # Основной запрос
    with django_assert_max_num_queries(2):
        response = authorized_client.get(athlete_list_url)
        assert response.status_code == status.HTTP_200_OK


# Остальные тесты API


@pytest.mark.django_db
def test_cancel_athlete(authorized_client, athlete):
    """Тест окончания действия роли спортсмена."""

    # Запрос на окончание действия роли
    response = authorized_client.post(
        get_api_url('athletes', 'cancel-athlete', pk=athlete.pk)
    )
    assert response.status_code == status.HTTP_200_OK

    # Проверяем, что действие роли спортсмена окончено
    athlete.refresh_from_db()
    assert athlete.date_to == now().date()

    # Проверяем, что если роль спортсмена уже недействующая, нельзя
    # окончить действие снова
    response = authorized_client.post(
        get_api_url('athletes', 'cancel-athlete', pk=athlete.pk)
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data[0] == (
        'Роль данного спортсмена уже не является действующей'
    )


# Тесты фильтрации и сортировки


@pytest.mark.parametrize(
    ('filter_param', 'expected_objects'),
    [
        ({'full_name': 'ив'}, [1, 0]),
        ({'full_name': 'Крис'}, [2]),
        ({'group_id': 99}, [0]),
    ],
)
@pytest.mark.django_db
def test_filters(
    authorized_client, athlete_list_url, filter_param, expected_objects
):
    """Тесты фильтрации списка спортсменов."""

    check_filters_and_ordering(
        athlete_list_url,
        authorized_client,
        create_athletes_filtering_test_data(),
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
    athlete_list_url,
    ordering_param,
    expected_objects,
):
    """Тесты сортировки списка спортсменов."""

    check_filters_and_ordering(
        athlete_list_url,
        authorized_client,
        create_athletes_filtering_test_data(),
        ordering_param,
        expected_objects,
    )
