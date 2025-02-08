from rest_framework import viewsets

from apps.person.api.filters import PersonFilter
from apps.person.api.serializers import PersonSerializer
from apps.person.models import Person


class PersonViewSet(viewsets.ModelViewSet):
    """API для работы с пользователями."""

    queryset = Person.objects.all().order_by('-id')
    serializer_class = PersonSerializer
    filterset_class = PersonFilter
