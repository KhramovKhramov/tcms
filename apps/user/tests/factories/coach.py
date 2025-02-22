import factory
from django.utils import timezone

from apps.user.models import Coach
from apps.user.models.choices import CoachPosition
from apps.user.tests.factories.user import UserFactory


class CoachFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    date_from = timezone.now().date()
    position = CoachPosition.INSTRUCTOR

    class Meta:
        model = Coach
