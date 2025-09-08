import factory
from apps.user.models import Coach
from apps.user.models.choices import CoachPosition
from django.utils.timezone import now

from tests.factories.user import UserFactory


class CoachFactory(factory.django.DjangoModelFactory):
    """Фабрика данных тренера."""

    user = factory.SubFactory(UserFactory)
    date_from = now().date()
    position = CoachPosition.INSTRUCTOR
    coach_experience = factory.Faker('random_digit')

    class Meta:
        model = Coach
