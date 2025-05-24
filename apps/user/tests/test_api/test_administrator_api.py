from datetime import date

import pytest
from conftest import check_filters_and_ordering, get_api_url
from django.conf import settings
from django.utils.timezone import now
from rest_framework import status

from apps.user.models import Administrator
from apps.user.tests.factories import AdministratorFactory, UserFactory
from apps.user.tests.test_api.utils import serialize_user


@pytest.mark.django_db
class TestAdministratorCRUDApi:
    """Тесты проверки CRUD-операций API администраторов."""

    model = Administrator
    factory = AdministratorFactory
    list_url = staticmethod(lambda: get_api_url('administrators', 'list'))

    @pytest.fixture
    def prepared_instances(self) -> list[Administrator]:
        """
        Фикстура, возвращающая список объектов
        модели для использования в тестах.
        """

        return self.factory.create_batch(5)

    @pytest.fixture
    def create_request_data(self) -> dict:
        """
        Фикстура, возвращающая словарь с данными, необходимыми для
        создания объекта модели.
        """

        instance = UserFactory.build()

        return {
            'user_data': {
                'email': instance.email,
                'first_name': instance.first_name,
                'last_name': instance.last_name,
                'date_of_birth': instance.date_of_birth,
                'gender': instance.gender,
                'phone': instance.phone,
            }
        }

    @staticmethod
    def _serialize_instance_detail(instance: Administrator) -> dict:
        """Сериализация объекта модели для метода retrieve()."""

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

    def _serialize_instance_list(self, instance: Administrator) -> dict:
        """Сериализация объекта модели для метода list()."""

        return self._serialize_instance_detail(instance)

    def _serialize_list(self, instances: list[Administrator]) -> list[dict]:
        """Сериализация списка объектов модели для метода list()."""

        return [
            self._serialize_instance_list(instance) for instance in instances
        ]

    def test_create(self, authorized_client, create_request_data) -> None:
        """Тест создания администратора вместе с пользователем."""

        response = authorized_client.post(
            self.list_url(),
            data=create_request_data,
            format='json',
        )
        assert response.status_code == status.HTTP_201_CREATED

        instance = self.model.objects.get(pk=response.data['id'])
        assert response.data == self._serialize_instance_detail(instance)

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

    cancel_administrator_url = staticmethod(
        lambda pk: get_api_url('administrators', 'cancel-administrator', pk=pk)
    )

    def test_cancel_administrator(self, authorized_client):
        """Тест окончания действия роли администратора."""

        # Создаем данные
        administrator = AdministratorFactory.create()

        # Проверяем окончание действия роли
        response = authorized_client.post(
            self.cancel_administrator_url(administrator.pk)
        )
        assert response.status_code == status.HTTP_200_OK

        # Проверяем, что действие роли администратора окончено
        administrator.refresh_from_db()
        assert administrator.date_to == now().date()

        # Проверяем, что если роль администратора уже недействующая, нельзя
        # окончить действие снова
        response = authorized_client.post(
            self.cancel_administrator_url(administrator.pk)
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data[0] == (
            'Роль данного администратора уже не является действующей'
        )


@pytest.mark.django_db
class TestAdministratorFilters:
    """Тесты фильтров и сортировки администраторов."""

    list_url = staticmethod(lambda: get_api_url('administrators', 'list'))

    @pytest.fixture
    def prepared_data(self) -> list[Administrator]:
        """
        Фикстура, возвращающая тестовые данные
        для проверки фильтрации и сортировки.
        """

        # Данные пользователей
        user_data = [
            {
                'last_name': 'Кривоногова',
                'first_name': 'Алевтина',
                'patronymic': 'Васильевна',
            },
            {
                'last_name': 'Иванов',
                'first_name': 'Иван',
                'patronymic': 'Иванович',
            },
            {
                'last_name': 'Большакова',
                'first_name': 'Кристина',
                'patronymic': 'Сергеевна',
            },
        ]

        # Создание пользователей
        users = [UserFactory.create(**data) for data in user_data]

        # Создаем и возвращаем администраторов для тестов
        return [
            AdministratorFactory.create(
                user=user,
            )
            for user in users
        ]

    @pytest.mark.parametrize(
        ('filter_param', 'expected_objects'),
        [
            ({'full_name': 'ив'}, [1, 0]),
            ({'full_name': 'Крис'}, [2]),
        ],
    )
    def test_filters(
        self, authorized_client, prepared_data, filter_param, expected_objects
    ):
        """Тесты фильтрации."""

        check_filters_and_ordering(
            self.list_url(),
            authorized_client,
            prepared_data,
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
    def test_ordering(
        self,
        authorized_client,
        prepared_data,
        ordering_param,
        expected_objects,
    ):
        """Тесты сортировки."""

        check_filters_and_ordering(
            self.list_url(),
            authorized_client,
            prepared_data,
            ordering_param,
            expected_objects,
        )
