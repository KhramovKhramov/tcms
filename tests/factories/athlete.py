import factory
from apps.user.models import Athlete
from common.choices import PlayingLevel
from django.utils.timezone import now

from tests.factories.user import UserFactory


class AthleteFactory(factory.django.DjangoModelFactory):
    """Фабрика данных спортсмена."""

    user = factory.SubFactory(UserFactory)
    date_from = now().date()
    playing_level = PlayingLevel.PLAYER

    class Meta:
        model = Athlete
