import pytest
from apps.user.models import Administrator, Athlete, Coach, User
from apps.user.models.choices import CoachPosition
from common.choices import PlayingLevel
from configs import settings
from django.utils.timezone import now
from rest_framework import status

from tests.factories import UserFactory
from tests.helpers import (
    create_user_request_data,
    serialize_user,
    update_user_request_data,
)
from tests.utils import get_api_url

# CRUD-тесты


@pytest.mark.django_db
def test_user_create(authorized_client, user_list_url):
    """Тест создания пользователя."""

    response = authorized_client.post(
        user_list_url, data=create_user_request_data()
    )
    assert response.status_code == status.HTTP_201_CREATED

    instance = User.objects.get(pk=response.data['id'])
    assert response.data == serialize_user(instance)


@pytest.mark.django_db
def test_user_update(authorized_client, user):
    """Тест обновления данных пользователя."""

    request_data = update_user_request_data()

    response = authorized_client.patch(
        get_api_url('users', 'detail', pk=user.pk), data=request_data
    )
    assert response.status_code == status.HTTP_200_OK

    user.refresh_from_db()
    assert response.data == serialize_user(user)

    for key, value in request_data.items():
        assert getattr(user, key) == value


@pytest.mark.django_db
def test_user_delete(authorized_client, user):
    """Тест удаления пользователя."""

    response = authorized_client.delete(
        get_api_url('users', 'detail', pk=user.pk)
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT

    assert not User.objects.filter(pk=user.pk).exists()


@pytest.mark.django_db
def test_user_retrieve(authorized_client, user):
    """Тест получения данных пользователя по идентификатору."""

    response = authorized_client.get(
        get_api_url('users', 'detail', pk=user.pk)
    )
    assert response.status_code == status.HTTP_200_OK

    assert response.data == serialize_user(user)


@pytest.mark.django_db
def test_users_list(authorized_client, user_list_url, users):
    """Тест получения списка пользователей."""

    response = authorized_client.get(user_list_url)
    assert response.status_code == status.HTTP_200_OK

    assert response.data['results'][0] == serialize_user(users[-1])


@pytest.mark.django_db
def test_users_list_pagination(authorized_client, user_list_url):
    """Тест пагинации в списке пользователей."""

    UserFactory.create_batch(30)

    response = authorized_client.get(user_list_url)
    assert response.status_code == status.HTTP_200_OK

    page_size = settings.REST_FRAMEWORK['PAGE_SIZE']
    assert len(response.data['results']) == page_size


@pytest.mark.django_db
def test_users_list_max_queries(
    authorized_client,
    user_list_url,
    users,
    django_assert_max_num_queries,
):
    """
    Тест проверки максимального количество запросов
    в списке пользователей.
    """

    # Количество записей для пагинации
    # Основной запрос
    with django_assert_max_num_queries(2):
        response = authorized_client.get(user_list_url)
        assert response.status_code == status.HTTP_200_OK


# Остальные тесты API


@pytest.mark.django_db
def test_appoint_administrator(authorized_client, user):
    """Тест проверки назначения пользователя администратором."""

    response = authorized_client.post(
        get_api_url('users', 'appoint-administrator', pk=user.pk)
    )
    assert response.status_code == status.HTTP_200_OK

    # Проверяем, что администратор создан
    assert Administrator.objects.filter(
        user=user, date_from=now().date(), date_to__isnull=True
    ).exists()

    # Проверяем, что если у пользователя уже есть действующая роль
    # администратора, создать еще одну нельзя
    response = authorized_client.post(
        get_api_url('users', 'appoint-administrator', pk=user.pk)
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data[0] == (
        'У пользователя уже есть действующая роль администратора'
    )


@pytest.mark.django_db
def test_appoint_coach(authorized_client, user):
    """Тест проверки назначения пользователя тренером."""

    request_data = {
        'position': CoachPosition.SENIOR,
        'coach_experience': 5,
        'achievements': 'Кандидат в мастера спорта',
    }

    # Создаем роль тренера с дефолтными данными
    response = authorized_client.post(
        get_api_url('users', 'appoint-coach', pk=user.pk)
    )
    assert response.status_code == status.HTTP_200_OK

    # Проверяем, что тренер создан
    coach = Coach.objects.filter(
        user=user, date_from=now().date(), date_to__isnull=True
    ).first()
    assert coach is not None

    # Удалим роль тренера и попробуем создать новую,
    # но с кастомными данными
    coach.delete()
    response = authorized_client.post(
        get_api_url('users', 'appoint-coach', pk=user.pk),
        data=request_data,
    )
    assert response.status_code == status.HTTP_200_OK

    # Проверяем, что тренер вновь создан и с нужными данными
    coach = Coach.objects.filter(
        user=user, date_from=now().date(), date_to__isnull=True
    ).first()
    assert coach is not None
    assert coach.position == CoachPosition.SENIOR
    assert coach.achievements == 'Кандидат в мастера спорта'
    assert coach.coach_experience == 5
    assert coach.current_coach_experience == 5

    # Проверяем, что если у пользователя уже есть действующая роль
    # тренера, создать еще одну нельзя
    response = authorized_client.post(
        get_api_url('users', 'appoint-coach', pk=user.pk)
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data[0] == (
        'У пользователя уже есть действующая роль тренера'
    )


@pytest.mark.django_db
def test_appoint_athlete(authorized_client, user):
    """Тест проверки назначения пользователя спортсменом."""

    request_data = {'playing_level': PlayingLevel.PLAYER}

    # Создаем роль спортсмена
    response = authorized_client.post(
        get_api_url('users', 'appoint-athlete', pk=user.pk),
        data=request_data,
    )
    assert response.status_code == status.HTTP_200_OK

    # Проверяем, что спортсмен создан и с нужными данными
    athlete = Athlete.objects.filter(
        user=user, date_from=now().date(), date_to__isnull=True
    ).first()
    assert athlete is not None
    assert athlete.playing_level == request_data['playing_level']

    # Проверяем, что если у пользователя уже есть действующая роль
    # спортсмена, создать еще одну нельзя
    response = authorized_client.post(
        get_api_url('users', 'appoint-athlete', pk=user.pk),
        data=request_data,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data[0] == (
        'У пользователя уже есть действующая роль спортсмена'
    )
