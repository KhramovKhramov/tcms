from django_filters import rest_framework as filters


class UserFilter(filters.FilterSet):
    """Фильтрация и сортировка пользователей."""

    # Фильтры
    email = filters.CharFilter(label='Email', lookup_expr='icontains')
    phone = filters.CharFilter(label='Номер телефона', lookup_expr='icontains')

    # Сортировка
    # TODO добавить фильтрацию и сортировку по ФИО
    # TODO Добавить фильтры по ролям
    ordering = filters.OrderingFilter(
        fields={'created_at': 'created_at'},
        field_labels={'created_at': 'Дата и время регистрации'},
    )
