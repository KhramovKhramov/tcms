import factory

from apps.user.models import User
from apps.user.models.choices import GenderType


class UserFactory(factory.django.DjangoModelFactory):
    """Фабрика данных пользователя."""

    last_name = factory.Faker('last_name_female', locale='ru_RU')
    first_name = factory.Faker('first_name_female', locale='ru_RU')
    date_of_birth = factory.Faker('date_of_birth', minimum_age=18)
    gender = GenderType.FEMALE

    # FIXME емейл должен генерироваться уникальный
    email = factory.Faker('email', domain='example.com', safe=True)
    phone = factory.Faker('numerify', text='+7(9##)###-####')

    class Meta:
        model = User
