from datetime import date

import pytest
from configs import settings
from conftest import check_filters_and_ordering, get_api_url
from django.utils.timezone import now
from rest_framework import status

from apps.training_process.tests.factories import GroupFactory
from apps.user.models import Athlete
from apps.user.tests.factories import AthleteFactory, UserFactory
from apps.user.tests.test_api.utils import serialize_user


@pytest.mark.django_db
class TestAthleteCRUDApi:
    """Тесты проверки CRUD-операций API спортсменов."""

    model = Athlete
    factory = AthleteFactory
    list_url = staticmethod(lambda: get_api_url('athletes', 'list'))
    detail_url = staticmethod(
        lambda pk: get_api_url('athletes', 'detail', pk=pk)
    )

    @pytest.fixture
    def prepared_instances(self) -> list[Athlete]:
        """
        Фикстура, возвращающая список объектов
        модели для использования в тестах.
        """

        return self.factory.create_batch(5)

    @pytest.fixture
    def prepared_instance(self, prepared_instances) -> Athlete:
        """Фикстура, возвращающая объект модели для использования в тестах."""

        return self.factory.create()

    @pytest.fixture
    def create_request_data(self) -> dict:
        """
        Фикстура, возвращающая словарь с данными, необходимыми для
        создания объекта модели.
        """

        user = UserFactory.build()
        athlete = AthleteFactory.build()

        return {
            'user_data': {
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'date_of_birth': user.date_of_birth,
                'gender': user.gender,
                'phone': user.phone,
            },
            'playing_level': athlete.playing_level,
        }

    @staticmethod
    def _serialize_instance_detail(instance: Athlete) -> dict:
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
            'playing_level': instance.playing_level,
        }

    def _serialize_instance_list(self, instance: Athlete) -> dict:
        """Сериализация объекта модели для метода list()."""

        return self._serialize_instance_detail(instance)

    def _serialize_list(self, instances: list[Athlete]) -> list[dict]:
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
class TestAthleteApi:
    """Тесты API тренеров."""

    cancel_athlete_url = staticmethod(
        lambda pk: get_api_url('athletes', 'cancel-athlete', pk=pk)
    )

    def test_cancel_athlete(self, authorized_client):
        """Тест окончания действия роли спортсмена."""

        # Создаем данные
        athlete = AthleteFactory.create()

        # Проверяем окончание действия роли
        response = authorized_client.post(self.cancel_athlete_url(athlete.pk))
        assert response.status_code == status.HTTP_200_OK

        # Проверяем, что действие роли спортсмена окончено
        athlete.refresh_from_db()
        assert athlete.date_to == now().date()

        # Проверяем, что если роль спортсмена уже недействующая, нельзя
        # окончить действие снова
        response = authorized_client.post(self.cancel_athlete_url(athlete.pk))
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data[0] == (
            'Роль данного спортсмена уже не является действующей'
        )


@pytest.mark.django_db
class TestAthleteFilters:
    """Тесты фильтров и сортировки спортсменов."""

    list_url = staticmethod(lambda: get_api_url('athletes', 'list'))

    @pytest.fixture
    def prepared_data(self, test_user) -> list[Athlete]:
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

        # Создание группы для тестирования фильтрации по группам
        group = GroupFactory.create(id=99, coach__user=test_user)

        # Создаем и возвращаем спортсменов для тестов
        athletes = [
            AthleteFactory.create(
                user=user,
            )
            for user in users
        ]
        athletes[0].groups.add(group)

        return athletes

    @pytest.mark.parametrize(
        ('filter_param', 'expected_objects'),
        [
            ({'full_name': 'ив'}, [1, 0]),
            ({'full_name': 'Крис'}, [2]),
            ({'group_id': 99}, [0]),
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
