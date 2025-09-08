import factory
from apps.user.models import Administrator
from django.utils.timezone import now

from tests.factories.user import UserFactory


class AdministratorFactory(factory.django.DjangoModelFactory):
    """Фабрика данных администратора."""

    user = factory.SubFactory(UserFactory)
    date_from = now().date()

    class Meta:
        model = Administrator
