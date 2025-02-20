import pytest
from conftest import check_filters_and_ordering, get_api_url
from django.conf import settings
from django.utils.timezone import now
from rest_framework import status

from apps.user.models import Administrator, User
from apps.user.tests.factories import UserFactory
from apps.user.tests.test_api.utils import serialize_user


@pytest.mark.django_db
class TestUserCRUDApi:
    """Тесты проверки CRUD-операций API пользователей."""

    model = User
    factory = UserFactory
    list_url = staticmethod(lambda: get_api_url('users', 'list'))
    detail_url = staticmethod(lambda pk: get_api_url('users', 'detail', pk=pk))

    @pytest.fixture
    def prepared_instances(self) -> list[User]:
        """
        Фикстура, возвращающая список объектов
        модели для использования в тестах.
        """

        return self.factory.create_batch(5)

    @pytest.fixture
    def prepared_instance(self, prepared_instances) -> User:
        """Фикстура, возвращающая объект модели для использования в тестах."""

        return prepared_instances[0]

    @pytest.fixture
    def create_request_data(self) -> dict:
        """
        Фикстура, возвращающая словарь с данными, необходимыми для
        создания объекта модели.
        """

        instance = self.factory.build()

        return {
            'email': instance.email,
            'password': 'password',
            'first_name': instance.first_name,
            'last_name': instance.last_name,
            'date_of_birth': instance.date_of_birth,
            'gender': instance.gender,
            'phone': instance.phone,
        }

    @pytest.fixture
    def update_request_data(self, create_request_data) -> dict:
        """
        Фикстура, возвращающая словарь с данными, необходимыми для
        обновления объекта модели.
        """

        update_fields = ['first_name', 'last_name']

        return {key: create_request_data[key] for key in update_fields}

    @staticmethod
    def _serialize_instance_detail(instance: User) -> dict:
        """Сериализация объекта модели для метода retrieve()."""

        return serialize_user(instance)

    def _serialize_instance_list(self, instance: User) -> dict:
        """Сериализация объекта модели для метода list()."""

        return self._serialize_instance_detail(instance)

    def _serialize_list(self, instances: list[User]) -> list[dict]:
        """Сериализация списка объектов модели для метода list()."""

        return [
            self._serialize_instance_list(instance) for instance in instances
        ]

    def test_create(self, authorized_client, create_request_data) -> None:
        """Тест создания."""

        response = authorized_client.post(
            self.list_url(), data=create_request_data
        )
        assert response.status_code == status.HTTP_201_CREATED

        instance = self.model.objects.get(pk=response.data['id'])
        assert response.data == self._serialize_instance_detail(instance)

    def test_update(
        self, authorized_client, prepared_instance, update_request_data
    ):
        """Тест обновления."""

        response = authorized_client.patch(
            self.detail_url(prepared_instance.pk),
            data=update_request_data,
        )
        assert response.status_code == status.HTTP_200_OK

        prepared_instance.refresh_from_db()
        assert response.data == self._serialize_instance_detail(
            prepared_instance
        )

        for key, value in update_request_data.items():
            assert getattr(prepared_instance, key) == value

    def test_delete(self, authorized_client, prepared_instance):
        """Тест удаления."""

        response = authorized_client.delete(
            self.detail_url(prepared_instance.pk)
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

        assert not self.model.objects.filter(pk=prepared_instance.pk).exists()

    def test_retrieve(self, authorized_client, prepared_instance):
        """Тест получения объекта по идентификатору."""

        response = authorized_client.get(self.detail_url(prepared_instance.pk))
        assert response.status_code == status.HTTP_200_OK

        assert response.data == self._serialize_instance_detail(
            prepared_instance
        )

    def test_list(self, authorized_client, prepared_instances, test_user):
        """Тест получения списка объектов."""

        response = authorized_client.get(self.list_url())
        assert response.status_code == status.HTTP_200_OK

        prepared_instances.insert(0, test_user)
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
class TestUserApi:
    """Тесты API пользователей."""

    appoint_administrator_url = staticmethod(
        lambda pk: get_api_url('users', 'appoint-administrator', pk=pk)
    )

    def test_appoint_administrator(self, authorized_client, test_user):
        """Тест проверки назначения пользователя администратором."""

        response = authorized_client.post(
            self.appoint_administrator_url(test_user.pk)
        )
        assert response.status_code == status.HTTP_200_OK

        # Проверяем, что администратор создан
        assert Administrator.objects.filter(
            user=test_user, date_from=now().date(), date_to__isnull=True
        ).exists()

        # Проверяем, что если у пользователя уже есть действующая роль
        # администратора, создать еще одну нельзя
        response = authorized_client.post(
            self.appoint_administrator_url(test_user.pk)
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data[0] == (
            'У пользователя уже есть действующая роль администратора'
        )


@pytest.mark.django_db
class TestUserFilters:
    """Тесты фильтров и сортировки пользователей."""

    list_url = staticmethod(lambda: get_api_url('users', 'list'))

    @pytest.fixture
    def prepared_data(self, test_user) -> list[User]:
        """
        Фикстура, возвращающая тестовые данные
        для проверки фильтрации и сортировки.
        """

        # Данные пользователей
        user_data = [
            {
                'last_name': 'Ученикова',
                'first_name': 'Елизавета',
                'patronymic': 'Вадимовна',
                'email': 'lizasergeevna@gmail.com',
                'phone': '+79129229090',
            },
            {
                'last_name': 'Сергеев',
                'first_name': 'Сергей',
                'patronymic': 'Сергеевич',
                'email': 'serg1992@mail.ru',
                'phone': '+79189996699',
            },
            {
                'last_name': 'Ничипорчук',
                'first_name': 'Александра',
                'patronymic': 'Александровна',
                'email': '9199228756@gmail.com',
                'phone': '+79199228756',
            },
        ]

        # Создаем и возвращаем пользователей для теста
        users = [UserFactory.create(**data) for data in user_data]
        users.insert(0, test_user)

        return users

    @pytest.mark.parametrize(
        # Учитываем в итоговом результате test_user из фикстуры авторизации
        ('filter_param', 'expected_objects'),
        [
            ({'full_name': 'Лиза'}, [1]),
            ({'full_name': 'вна'}, [3, 1]),
            ({'email': 'serg'}, [2, 1]),
            ({'phone': '912'}, [1]),
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
        # Учитываем в итоговом результате test_user из фикстуры авторизации
        ('ordering_param', 'expected_objects'),
        [
            ({'ordering': ''}, [3, 2, 1, 0]),
            ({'ordering': 'full_name'}, [3, 2, 0, 1]),
            ({'ordering': '-full_name'}, [1, 0, 2, 3]),
            ({'ordering': 'created_at'}, [0, 1, 2, 3]),
            ({'ordering': '-created_at'}, [3, 2, 1, 0]),
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
