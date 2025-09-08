import pytest
from apps.user.models import Administrator, Athlete, Coach, User

from tests.factories import (
    AdministratorFactory,
    AthleteFactory,
    CoachFactory,
    UserFactory,
)
from tests.utils import get_api_url

# Фикстуры urls


@pytest.fixture(scope='session')
def user_list_url() -> str:
    return get_api_url('users', 'list')


@pytest.fixture(scope='session')
def administrator_list_url() -> str:
    return get_api_url('administrators', 'list')


@pytest.fixture(scope='session')
def athlete_list_url() -> str:
    return get_api_url('athletes', 'list')


@pytest.fixture(scope='session')
def coach_list_url() -> str:
    return get_api_url('coaches', 'list')


# Фикстуры объектов


@pytest.fixture
def user() -> User:
    return UserFactory.create()


@pytest.fixture
def users() -> list[User]:
    return UserFactory.create_batch(5)


@pytest.fixture
def administrator() -> Administrator:
    return AdministratorFactory.create()


@pytest.fixture
def administrators() -> list[Administrator]:
    return AdministratorFactory.create_batch(5)


@pytest.fixture
def athlete() -> Athlete:
    return AthleteFactory.create()


@pytest.fixture
def athletes() -> list[Athlete]:
    return AthleteFactory.create_batch(5)


@pytest.fixture
def coach() -> Coach:
    return CoachFactory.create()


@pytest.fixture
def coaches() -> list[Coach]:
    return CoachFactory.create_batch(5)
