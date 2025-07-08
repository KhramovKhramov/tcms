import pytest
from configs import settings
from conftest import check_filters_and_ordering, get_api_url
from django.utils.timezone import now
from rest_framework import status

from apps.user.models import Coach
from apps.user.models.choices import CoachPosition
from apps.user.tests.factories import CoachFactory, UserFactory
from apps.user.tests.test_api.utils import serialize_coach


@pytest.mark.django_db
class TestCoachCRUDApi:
    """Тесты проверки CRUD-операций API тренеров."""

    model = Coach
    factory = CoachFactory
    list_url = staticmethod(lambda: get_api_url('coaches', 'list'))
    detail_url = staticmethod(
        lambda pk: get_api_url('coaches', 'detail', pk=pk)
    )

    @pytest.fixture
    def prepared_instances(self) -> list[Coach]:
        """
        Фикстура, возвращающая список объектов
        модели для использования в тестах.
        """

        return self.factory.create_batch(5)

    @pytest.fixture
    def prepared_instance(self, prepared_instances) -> Coach:
        """Фикстура, возвращающая объект модели для использования в тестах."""

        return self.factory.create()

    @pytest.fixture
    def create_request_data(self) -> dict:
        """
        Фикстура, возвращающая словарь с данными, необходимыми для
        создания объекта модели.
        """

        user = UserFactory.build()
        coach = CoachFactory.build()

        return {
            'user_data': {
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'date_of_birth': user.date_of_birth,
                'gender': user.gender,
                'phone': user.phone,
            },
            'position': coach.position,
            'coach_experience': coach.coach_experience,
        }

    @staticmethod
    def _serialize_instance_detail(instance: Coach) -> dict:
        """Сериализация объекта модели для метода retrieve()."""

        return serialize_coach(instance)

    def _serialize_instance_list(self, instance: Coach) -> dict:
        """Сериализация объекта модели для метода list()."""

        return self._serialize_instance_detail(instance)

    def _serialize_list(self, instances: list[Coach]) -> list[dict]:
        """Сериализация списка объектов модели для метода list()."""

        return [
            self._serialize_instance_list(instance) for instance in instances
        ]

    def test_create(self, authorized_client, create_request_data) -> None:
        """Тест создания спортсмена вместе с пользователем."""

        response = authorized_client.post(
            self.list_url(),
            data=create_request_data,
            format='json',
        )
        assert response.status_code == status.HTTP_201_CREATED

        instance = self.model.objects.get(pk=response.data['id'])
        assert response.data == self._serialize_instance_detail(instance)

    def test_retrieve(self, authorized_client, prepared_instance):
        """Тест получения объекта по идентификатору."""

        response = authorized_client.get(self.detail_url(prepared_instance.pk))
        assert response.status_code == status.HTTP_200_OK

        assert response.data == self._serialize_instance_detail(
            prepared_instance
        )

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
class TestCoachApi:
    """Тесты API тренеров."""

    cancel_coach_url = staticmethod(
        lambda pk: get_api_url('coaches', 'cancel-coach', pk=pk)
    )

    def test_cancel_coach(self, authorized_client):
        """Тест окончания действия роли тренера."""

        # Создаем данные
        coach = CoachFactory.create()

        # Проверяем окончание действия роли
        response = authorized_client.post(self.cancel_coach_url(coach.pk))
        assert response.status_code == status.HTTP_200_OK

        # Проверяем, что действие роли тренера окончено
        coach.refresh_from_db()
        assert coach.date_to == now().date()

        # Проверяем, что если роль тренера уже недействующая, нельзя
        # окончить действие снова
        response = authorized_client.post(self.cancel_coach_url(coach.pk))
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data[0] == (
            'Роль данного тренера уже не является действующей'
        )


@pytest.mark.django_db
class TestCoachFilters:
    """Тесты фильтров и сортировки тренеров."""

    list_url = staticmethod(lambda: get_api_url('coaches', 'list'))

    @pytest.fixture
    def prepared_data(self) -> list[Coach]:
        """
        Фикстура, возвращающая тестовые данные
        для проверки фильтрации и сортировки.
        """

        # Данные пользователей
        user_data = [
            {
                'last_name': 'Суплотова',
                'first_name': 'Людмила',
                'patronymic': 'Александровна',
            },
            {
                'last_name': 'Брельгин',
                'first_name': 'Макар',
                'patronymic': 'Игоревич',
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
            CoachFactory.create(
                user=users[0],
                position=CoachPosition.INSTRUCTOR,
                coach_experience=5,
            ),
            CoachFactory.create(
                user=users[1],
                position=CoachPosition.INSTRUCTOR,
                coach_experience=3,
            ),
            CoachFactory.create(
                user=users[2],
                position=CoachPosition.SENIOR,
                coach_experience=8,
            ),
        ]

    @pytest.mark.parametrize(
        ('filter_param', 'expected_objects'),
        [
            ({'full_name': 'ак'}, [2, 1]),
            ({'full_name': 'Макар'}, [1]),
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
            ({'ordering': 'position'}, [0, 1, 2]),
            ({'ordering': '-position'}, [2, 0, 1]),
            ({'ordering': 'all_coach_experience'}, [1, 0, 2]),
            ({'ordering': '-all_coach_experience'}, [2, 0, 1]),
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
