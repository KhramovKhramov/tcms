import factory

from apps.training_process.models import GroupApplication
from apps.training_process.models.choices import PlayingLevel
from apps.training_process.tests.factories.group import GroupFactory
from apps.user.tests.factories import UserFactory


class GroupApplicationFactory(factory.django.DjangoModelFactory):
    """Фабрика данных заявки на присоединение к группе."""

    user = factory.SubFactory(UserFactory)
    group = factory.SubFactory(GroupFactory)
    playing_level = PlayingLevel.PLAYER
    comment = factory.Faker('text')

    class Meta:
        model = GroupApplication
