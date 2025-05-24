from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.user.api.filters import AthleteFilter
from apps.user.api.serializers import AthleteSerializer
from apps.user.models import Athlete
from apps.user.services import AthleteCancelService


class AthleteViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    """API для работы со спортсменами."""

    # TODO если у пользователя несколько ролей спортсмена,
    #  должна показываться только последняя
    queryset = Athlete.objects.all().order_by('-id').select_related('user')
    serializer_class = AthleteSerializer
    filterset_class = AthleteFilter

    @extend_schema(
        summary='Окончание действия роли спортсмена',
        request=None,
        responses={
            status.HTTP_200_OK: AthleteSerializer,
        },
        parameters=[
            OpenApiParameter(
                name='id',
                type=int,
                location=OpenApiParameter.PATH,
                description='ID спортсмена',
            ),
        ],
    )
    @action(
        detail=True,
        methods=['POST'],
        url_path='cancel-athlete',
        url_name='cancel-athlete',
    )
    def cancel_athlete(self, request, *args, **kwargs):
        """
        Окончание действия роли спортсмена.

        Если роль спортсмена действующая, в поле окончания действия роли
        будет указана текущая дата, и роль перестанет быть действующей.
        """

        athlete = self.get_object()
        athlete = AthleteCancelService(athlete).execute()

        response_serializer = AthleteSerializer(athlete)
        return Response(response_serializer.data, status=status.HTTP_200_OK)
