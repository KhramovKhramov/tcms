from datetime import timedelta

import factory
from common.choices import PlayingLevel, Weekdays
from django.utils.timezone import now

from apps.training_process.models import Group
from apps.training_process.models.choices import GroupStatus
from apps.user.tests.factories import CoachFactory


class GroupFactory(factory.django.DjangoModelFactory):
    """Фабрика данных группы."""

    name = factory.Faker('word')
    status = GroupStatus.ACTIVE
    coach = factory.SubFactory(CoachFactory)
    playing_level = PlayingLevel.PLAYER
    training_days = [Weekdays.MONDAY, Weekdays.WEDNESDAY]
    training_time = '19:00'
    trainings_start_date = now().date() + timedelta(days=21)

    class Meta:
        model = Group
