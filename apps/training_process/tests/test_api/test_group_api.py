import pytest
from configs import settings
from conftest import get_api_url
from rest_framework import status

from apps.training_process.models import Group
from apps.training_process.tests.factories import GroupFactory
from apps.user.tests.factories import CoachFactory
from apps.user.tests.test_api.utils import serialize_coach


@pytest.mark.django_db
class TestGroupCRUDApi:
    """Тесты проверки CRUD-операций API групп."""

    model = Group
    factory = GroupFactory
    list_url = staticmethod(lambda: get_api_url('groups', 'list'))
    detail_url = staticmethod(
        lambda pk: get_api_url('groups', 'detail', pk=pk)
    )

    @pytest.fixture
    def prepared_instances(self) -> list[Group]:
        """
        Фикстура, возвращающая список объектов
        модели для использования в тестах.
        """

        coach = CoachFactory.create()
        return self.factory.create_batch(5, coach=coach)

    @pytest.fixture
    def prepared_instance(self, prepared_instances) -> Group:
        """Фикстура, возвращающая объект модели для использования в тестах."""

        return prepared_instances[0]

    @pytest.fixture
    def create_request_data(self) -> dict:
        """
        Фикстура, возвращающая словарь с данными, необходимыми для
        создания объекта модели.
        """

        coach = CoachFactory.create()
        instance = self.factory.build()

        return {
            'name': instance.name,
            'status': instance.status,
            'coach_id': coach.pk,
            'min_participants': instance.min_participants,
            'max_participants': instance.max_participants,
            'playing_level': instance.playing_level,
            'training_days': instance.training_days,
            'training_time': instance.training_time,
            'trainings_start_date': instance.trainings_start_date,
        }

    @pytest.fixture
    def update_request_data(self, create_request_data) -> dict:
        """
        Фикстура, возвращающая словарь с данными, необходимыми для
        обновления объекта модели.
        """

        return create_request_data

    @staticmethod
    def _serialize_instance_detail(instance: Group) -> dict:
        """Сериализация объекта модели для метода retrieve()."""

        return {
            'id': instance.pk,
            'name': instance.name,
            'description': instance.description,
            'status': instance.status,
            'coach': serialize_coach(instance.coach),
            'min_participants': instance.min_participants,
            'max_participants': instance.max_participants,
            'playing_level': instance.playing_level,
            'training_days': instance.training_days,
            'training_time': instance.training_time,
            'trainings_start_date': instance.trainings_start_date.strftime(
                '%Y-%m-%d'
            ),
        }

    def _serialize_instance_list(self, instance: Group) -> dict:
        """Сериализация объекта модели для метода list()."""

        return self._serialize_instance_detail(instance)

    def _serialize_list(self, instances: list[Group]) -> list[dict]:
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

        coach = CoachFactory.create()
        self.factory.create_batch(30, coach=coach)

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
