from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.user.api.filters import CoachFilter
from apps.user.api.serializers import CoachCreateSerializer, CoachSerializer
from apps.user.models import Coach
from apps.user.services import CoachCancelService, CoachWithUserCreateService


class CoachViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    """API для работы с тренерами."""

    # TODO если у пользователя несколько ролей тренера,
    #  должна показываться только последняя
    queryset = Coach.objects.all().order_by('-id').select_related('user')

    serializer_class = CoachSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return CoachCreateSerializer
        return super().get_serializer_class()

    filterset_class = CoachFilter

    @extend_schema(
        summary='Создание роли тренера вместе с пользователем',
        request=CoachCreateSerializer,
        responses={
            status.HTTP_201_CREATED: CoachSerializer,
        },
    )
    def create(self, request, *args, **kwargs):
        """
        Создание роли тренера вместе с созданием нового для системы
        пользователя.
        """

        request_serializer = self.get_serializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        coach = CoachWithUserCreateService(
            **request_serializer.validated_data
        ).execute()

        response_serializer = CoachSerializer(coach)
        return Response(
            response_serializer.data, status=status.HTTP_201_CREATED
        )

    @extend_schema(
        summary='Окончание действия роли тренера',
        request=None,
        responses={
            status.HTTP_200_OK: CoachSerializer,
        },
        parameters=[
            OpenApiParameter(
                name='id',
                type=int,
                location=OpenApiParameter.PATH,
                description='ID тренера',
            ),
        ],
    )
    @action(
        detail=True,
        methods=['POST'],
        url_path='cancel-coach',
        url_name='cancel-coach',
    )
    def cancel_coach(self, request, *args, **kwargs):
        """
        Окончание действия роли тренера.

        Если роль тренера действующая, в поле окончания действия роли
        будет указана текущая дата, и роль перестанет быть действующей.
        """

        coach = self.get_object()
        coach = CoachCancelService(coach).execute()

        response_serializer = CoachSerializer(coach)
        return Response(response_serializer.data, status=status.HTTP_200_OK)
