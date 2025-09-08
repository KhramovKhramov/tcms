import factory
from apps.training_process.models import GroupApplication
from common.choices import PlayingLevel

from tests.factories.group import GroupFactory
from tests.factories.user import UserFactory


class GroupApplicationFactory(factory.django.DjangoModelFactory):
    """Фабрика данных заявки на присоединение к группе."""

    user = factory.SubFactory(UserFactory)
    group = factory.SubFactory(GroupFactory)
    playing_level = PlayingLevel.PLAYER
    comment = factory.Faker('text')

    class Meta:
        model = GroupApplication
