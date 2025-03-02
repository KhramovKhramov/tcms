import pytest
from configs import settings
from conftest import check_filters_and_ordering, get_api_url
from rest_framework import status

from apps.training_process.models import Group, GroupApplication
from apps.training_process.models.choices import GroupApplicationStatus
from apps.training_process.tests.factories import (
    GroupApplicationFactory,
    GroupFactory,
)
from apps.training_process.tests.test_api.utils import serialize_group
from apps.user.models import Athlete
from apps.user.tests.factories import CoachFactory, UserFactory
from apps.user.tests.test_api.utils import serialize_user


@pytest.fixture
def training_group() -> Group:
    """
    Фикстура, возвращающая тренировочную группу для использования в тестах.
    """

    return GroupFactory.create()


@pytest.mark.django_db
class TestGroupApplicationCRUDApi:
    """
    Тесты проверки CRUD-операций API
    заявок на присоединение к тренировочной группе.
    """

    model = GroupApplication
    factory = GroupApplicationFactory
    list_url = staticmethod(lambda: get_api_url('group-applications', 'list'))
    detail_url = staticmethod(
        lambda pk: get_api_url('group-applications', 'detail', pk=pk)
    )

    @pytest.fixture
    def prepared_instances(self, training_group) -> list[GroupApplication]:
        """
        Фикстура, возвращающая список объектов
        модели для использования в тестах.
        """

        return self.factory.create_batch(5, group=training_group)

    @pytest.fixture
    def prepared_instance(self, prepared_instances) -> GroupApplication:
        """Фикстура, возвращающая объект модели для использования в тестах."""

        return prepared_instances[0]

    @pytest.fixture
    def create_request_data(self, training_group, test_user) -> dict:
        """
        Фикстура, возвращающая словарь с данными, необходимыми для
        создания объекта модели.
        """

        instance = self.factory.build()

        return {
            'group_id': training_group.pk,
            'user_id': test_user.pk,
            'playing_level': instance.playing_level,
            'comment': instance.comment,
        }

    @pytest.fixture
    def update_request_data(self, create_request_data) -> dict:
        """
        Фикстура, возвращающая словарь с данными, необходимыми для
        обновления объекта модели.
        """

        update_fields = ['playing_level', 'comment']

        return {key: create_request_data[key] for key in update_fields}

    @staticmethod
    def _serialize_instance_detail(instance: GroupApplication) -> dict:
        """Сериализация объекта модели для метода retrieve()."""

        return {
            'id': instance.pk,
            'user': serialize_user(instance.user),
            'group': serialize_group(instance.group),
            'status': instance.status,
            'created_at': instance.created_at.isoformat().replace(
                '+00:00', 'Z'
            ),
            'playing_level': instance.playing_level,
            'comment': instance.comment,
            'reject_reason': instance.reject_reason,
        }

    def _serialize_instance_list(self, instance: GroupApplication) -> dict:
        """Сериализация объекта модели для метода list()."""

        return self._serialize_instance_detail(instance)

    def _serialize_list(self, instances: list[GroupApplication]) -> list[dict]:
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
class TestGroupApplicationApi:
    """Тесты API заявок на присоединение к тренировочной группе."""

    reject_application_url = staticmethod(
        lambda pk: get_api_url('group-applications', 'reject', pk=pk)
    )
    approve_application_url = staticmethod(
        lambda pk: get_api_url('group-applications', 'approve', pk=pk)
    )

    def test_reject_group_application(
        self, authorized_client, test_user, training_group
    ):
        """Тест отклонения заявки на присоединение к группе."""

        # Создаем данные
        group_application = GroupApplicationFactory.create(
            group=training_group,
            user=test_user,
        )
        reject_reason = 'Потому что'

        # Отклоняем заявку
        response = authorized_client.post(
            self.reject_application_url(group_application.pk),
            data={
                'reject_reason': reject_reason,
            },
        )
        assert response.status_code == status.HTTP_200_OK

        group_application.refresh_from_db()

        assert group_application.reject_reason == reject_reason
        assert group_application.status == GroupApplicationStatus.REJECT

        # Отправляем запрос еще раз и проверяем, что из другого статуса заявку
        # отклонить нельзя
        response = authorized_client.post(
            self.reject_application_url(group_application.pk),
            data={
                'reject_reason': reject_reason,
            },
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data[0] == (
            'Отклонять можно только заявки в статусе "Новая"'
        )

    def test_approve_group_application(
        self, authorized_client, test_user, training_group
    ):
        """Тест одобрения заявки на присоединение к группе."""

        # Создаем данные
        group_application = GroupApplicationFactory.create(
            group=training_group,
            user=test_user,
        )

        # Одобряем заявку
        response = authorized_client.post(
            self.approve_application_url(group_application.pk),
        )
        assert response.status_code == status.HTTP_200_OK

        # Проверяем, что заявка одобрена
        group_application.refresh_from_db()
        assert group_application.status == GroupApplicationStatus.APPROVED

        # Проверяем, что создан спортсмен и присоединен к группе
        athlete = Athlete.objects.filter(
            user=test_user,
            date_to__isnull=True,
        ).first()

        assert athlete is not None
        assert training_group in athlete.groups.all()

        # Отправляем запрос еще раз и проверяем, что из другого статуса заявку
        # одобрить нельзя
        response = authorized_client.post(
            self.approve_application_url(group_application.pk),
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data[0] == (
            'Одобрять можно только заявки в статусе "Новая"'
        )

        # TODO добавить проверку - если у пользователя была действующая роль
        #  спортсмена - используется она


@pytest.mark.django_db
class TestTestGroupApplicationFilters:
    """Тесты фильтров и сортировки заявок на присоединение к группе."""

    list_url = staticmethod(lambda: get_api_url('group-applications', 'list'))

    @pytest.fixture
    def prepared_data(self, test_user) -> list[GroupApplication]:
        """
        Фикстура, возвращающая тестовые данные
        для проверки фильтрации и сортировки.
        """

        # Данные пользователей
        user_data = [
            {
                'id': 99,
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

        # Создание групп для подачи заявок
        coach = CoachFactory.create(user=test_user)
        group1 = GroupFactory.create(id=99, coach=coach)
        group2 = GroupFactory.create(coach=coach)

        # Создаем и возвращаем администраторов для тестов
        return [
            GroupApplicationFactory.create(
                user=users[0],
                group=group1,
            ),
            GroupApplicationFactory.create(
                user=users[1],
                group=group1,
            ),
            GroupApplicationFactory.create(
                user=users[2],
                group=group2,
            ),
        ]

    @pytest.mark.parametrize(
        ('filter_param', 'expected_objects'),
        [
            ({'full_name': 'ив'}, [1, 0]),
            ({'full_name': 'Крис'}, [2]),
            ({'user_id': 99}, [0]),
            ({'group_id': 99}, [1, 0]),
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
            ({'ordering': 'created_at'}, [0, 1, 2]),
            ({'ordering': '-created_at'}, [2, 1, 0]),
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
