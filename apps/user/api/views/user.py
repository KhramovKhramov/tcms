from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.user.api.filters import UserFilter
from apps.user.api.serializers import (
    AdministratorSerializer,
    AppointAthleteSerializer,
    AppointCoachSerializer,
    AthleteSerializer,
    CoachSerializer,
    UserSerializer,
)
from apps.user.models import User
from apps.user.services import (
    UserAppointAdministratorService,
    UserAppointAthleteService,
    UserAppointCoachService,
)


class UserViewSet(viewsets.ModelViewSet):
    """API для работы с пользователями."""

    queryset = User.objects.all().order_by('-id')

    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.action == 'appoint_coach':
            return AppointCoachSerializer
        if self.action == 'appoint_athlete':
            return AppointAthleteSerializer
        return super().get_serializer_class()

    filterset_class = UserFilter
    http_method_names = ['get', 'post', 'patch', 'delete']

    @extend_schema(
        summary='Назначение пользователю роли администратора',
        request=None,
        responses={
            status.HTTP_200_OK: AdministratorSerializer,
        },
        parameters=[
            OpenApiParameter(
                name='id',
                type=int,
                location=OpenApiParameter.PATH,
                description='ID пользователя, которому'
                'назначается роль администратора',
            ),
        ],
    )
    @action(
        detail=True,
        methods=['POST'],
        url_path='appoint-administrator',
        url_name='appoint-administrator',
    )
    def appoint_administrator(self, request, *args, **kwargs):
        """
        Назначение пользователю роли администратора.

        У пользователя не должно быть действующей роли администратора, иначе
        будет ошибка. Если действующей роли нет, будет создана запись в
        таблице администраторов с привязанным пользователем.
        """

        user = self.get_object()
        administrator = UserAppointAdministratorService(user).execute()

        response_serializer = AdministratorSerializer(administrator)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary='Назначение пользователю роли тренера',
        request=AppointCoachSerializer(),
        responses={
            status.HTTP_200_OK: CoachSerializer,
        },
        parameters=[
            OpenApiParameter(
                name='id',
                type=int,
                location=OpenApiParameter.PATH,
                description='ID пользователя, которому'
                'назначается роль тренера',
            ),
        ],
    )
    @action(
        detail=True,
        methods=['POST'],
        url_path='appoint-coach',
        url_name='appoint-coach',
    )
    def appoint_coach(self, request, *args, **kwargs):
        """
        Назначение пользователю роли тренера.

        У пользователя не должно быть действующей роли тренера, иначе
        будет ошибка. Если действующей роли нет, будет создана запись в
        таблице тренеров с привязанным пользователем.
        """

        user = self.get_object()
        request_serializer = self.get_serializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        coach = UserAppointCoachService(
            user=user, data=request_serializer.validated_data
        ).execute()

        response_serializer = CoachSerializer(coach)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary='Назначение пользователю роли спортсмена',
        request=AppointAthleteSerializer(),
        responses={
            status.HTTP_200_OK: AthleteSerializer,
        },
        parameters=[
            OpenApiParameter(
                name='id',
                type=int,
                location=OpenApiParameter.PATH,
                description='ID пользователя, которому'
                'назначается роль спортсмена',
            ),
        ],
    )
    @action(
        detail=True,
        methods=['POST'],
        url_path='appoint-athlete',
        url_name='appoint-athlete',
    )
    def appoint_athlete(self, request, *args, **kwargs):
        """
        Назначение пользователю роли спортсмена.

        У пользователя не должно быть действующей роли спортсмена, иначе
        будет ошибка. Если действующей роли нет, будет создана запись в
        таблице спортсменов с привязанным пользователем.
        """

        user = self.get_object()
        request_serializer = self.get_serializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        athlete = UserAppointAthleteService(
            user=user, **request_serializer.validated_data
        ).execute()

        response_serializer = AthleteSerializer(athlete)
        return Response(response_serializer.data, status=status.HTTP_200_OK)
