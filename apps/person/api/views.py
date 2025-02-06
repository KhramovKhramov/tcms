from rest_framework import viewsets

from apps.person.models import Person
from apps.person.api.serializers import PersonSerializer


class PersonViewSet(viewsets.ModelViewSet):
    """API для работы с пользователями."""

    queryset = Person.objects.all().order_by('-id')
    serializer_class = PersonSerializer
