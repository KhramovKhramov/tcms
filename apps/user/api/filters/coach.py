from common.mixins import FullNameFilterMixin
from django_filters import rest_framework as filters
from django_filters.constants import EMPTY_VALUES


class CoachOrderingFilter(filters.OrderingFilter):
    """
    Класс сортировки для модели Coach.

    Обновляет стандартный OrderingFilter, добавляя к кверисету аннотации.
    """

    def filter(self, qs, value):
        if value in EMPTY_VALUES:
            return qs

        ordering = [
            self.get_ordering_value(param)
            for param in value
            if param not in EMPTY_VALUES
        ]
        return (
            qs.with_full_name_annotation()
            .with_all_coach_experience_annotation()
            .order_by(*ordering)
        )


class CoachFilter(FullNameFilterMixin):
    """Фильтрация и сортировка тренеров."""

    # Сортировка
    # TODO добавить сортировку по стажу работы
    ordering = CoachOrderingFilter(
        fields={
            'full_name': 'full_name',
            'position': 'position',
            'all_coach_experience': 'all_coach_experience',
        },
        field_labels={
            'full_name': 'ФИО пользователя',
            'position': 'Должность',
            'all_coach_experience': 'Общий тренерский стаж',
        },
    )
