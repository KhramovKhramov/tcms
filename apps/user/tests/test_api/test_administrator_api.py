from datetime import date

import pytest
from conftest import get_api_url
from django.conf import settings
from rest_framework import status

from apps.user.models import Administrator
from apps.user.tests.factories import AdministratorFactory
from apps.user.tests.test_api.utils import serialize_user


@pytest.mark.django_db
class TestAdministratorCRUDApi:
    """Тесты проверки CRUD-операций API администраторов."""

    model = Administrator
    factory = AdministratorFactory
    list_url = staticmethod(lambda: get_api_url('administrators'))

    @pytest.fixture
    def prepared_instances(self) -> list[Administrator]:
        """
        Фикстура, возвращающая список объектов
        модели для использования в тестах.
        """

        return self.factory.create_batch(5)

    @staticmethod
    def _serialize_instance_list(instance: Administrator) -> dict:
        """Сериализация объекта модели для метода list()."""

        return {
            'id': instance.pk,
            'user': serialize_user(instance.user),
            'date_from': instance.date_from.strftime('%Y-%m-%d')
            if isinstance(instance.date_from, date)
            else instance.date_from,
            'date_to': instance.date_to.strftime('%Y-%m-%d')
            if isinstance(instance.date_to, date)
            else instance.date_to,
        }

    def _serialize_list(self, instances: list[Administrator]) -> list[dict]:
        """Сериализация списка объектов модели для метода list()."""

        return [
            self._serialize_instance_list(instance) for instance in instances
        ]

    def test_list(self, authorized_client, prepared_instances):
        """Тест получения списка объектов."""

        response = authorized_client.get(self.list_url())
        assert response.status_code == status.HTTP_200_OK

        assert response.data['results'] == self._serialize_list(
            prepared_instances[::-1]
        )

    def test_pagination(self, authorized_client):
        """Тест пагинации."""

        self.factory.create_batch(30)

        response = authorized_client.get(self.list_url())
        assert response.status_code == status.HTTP_200_OK

        page_size = settings.REST_FRAMEWORK['PAGE_SIZE']
        assert len(response.data['results']) == page_size

    def test_max_queries(
        self,
        authorized_client,
        prepared_instances,
        django_assert_max_num_queries,
    ):
        """Тест проверки максимального количество запросов."""

        # Количество записей для пагинации
        # Основной запрос
        with django_assert_max_num_queries(2):
            response = authorized_client.get(self.list_url())
            assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestAdministratorApi:
    """Тесты API администраторов."""

    # TODO добавить тест на окончание роли администратора
