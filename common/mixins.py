from django_filters import rest_framework as filters

class FullNameFilterMixin(filters.FilterSet):
    """Добавляет к классу с фильтрами фильтр по ФИО пользователя."""

    full_name = filters.CharFilter(
        label='ФИО пользователя', method='full_name_filter'
    )

    @staticmethod
    def full_name_filter(qs, name, value):
        """Фильтрация по ФИО пользователя."""

        return qs.with_full_name_annotation().filter(
            full_name__icontains=value,
        )