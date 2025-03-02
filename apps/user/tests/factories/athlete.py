import factory
from common.choices import PlayingLevel
from django.utils import timezone

from apps.user.models import Athlete
from apps.user.tests.factories.user import UserFactory


class AthleteFactory(factory.django.DjangoModelFactory):
    """Фабрика данных спортсмена."""

    user = factory.SubFactory(UserFactory)
    date_from = timezone.now().date()
    playing_level = PlayingLevel.PLAYER

    class Meta:
        model = Athlete
