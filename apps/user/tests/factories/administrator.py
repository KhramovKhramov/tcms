import factory
from django.utils import timezone

from apps.user.models import Administrator
from apps.user.tests.factories.user import UserFactory


class AdministratorFactory(factory.django.DjangoModelFactory):
    """Фабрика данных администратора."""

    user = factory.SubFactory(UserFactory)
    date_from = timezone.now().date()

    class Meta:
        model = Administrator
