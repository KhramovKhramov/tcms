from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.user.api.filters import AdministratorFilter
from apps.user.api.serializers import (
    AdministratorCreateSerializer,
    AdministratorSerializer,
)
from apps.user.models import Administrator
from apps.user.services import (
    AdministratorCancelService,
    AdministratorWithUserCreateService,
)


class AdministratorViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet
):
    """API для работы с администраторами."""

    # TODO если у пользователя несколько ролей администратора,
    #  должна показываться только последняя
    queryset = (
        Administrator.objects.all().order_by('-id').select_related('user')
    )

    serializer_class = AdministratorSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return AdministratorCreateSerializer
        return super().get_serializer_class()

    filterset_class = AdministratorFilter

    @extend_schema(
        summary='Создание роли администратора вместе с пользователем',
        request=AdministratorCreateSerializer,
        responses={
            status.HTTP_201_CREATED: AdministratorSerializer,
        },
    )
    def create(self, request, *args, **kwargs):
        """
        Создание роли администратора вместе с созданием нового для системы
        пользователя.
        """

        request_serializer = self.get_serializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        administrator = AdministratorWithUserCreateService(
            **request_serializer.validated_data
        ).execute()

        response_serializer = AdministratorSerializer(administrator)
        return Response(
            response_serializer.data, status=status.HTTP_201_CREATED
        )

    @extend_schema(
        summary='Окончание действия роли администратора',
        request=None,
        responses={
            status.HTTP_200_OK: AdministratorSerializer,
        },
        parameters=[
            OpenApiParameter(
                name='id',
                type=int,
                location=OpenApiParameter.PATH,
                description='ID администратора',
            ),
        ],
    )
    @action(
        detail=True,
        methods=['POST'],
        url_path='cancel-administrator',
        url_name='cancel-administrator',
    )
    def cancel_administrator(self, request, *args, **kwargs):
        """
        Окончание действия роли администратора.

        Если роль администратора действующая, в поле окончания действия роли
        будет указана текущая дата, и роль перестанет быть действующей.
        """

        administrator = self.get_object()
        administrator = AdministratorCancelService(administrator).execute()

        response_serializer = AdministratorSerializer(administrator)
        return Response(response_serializer.data, status=status.HTTP_200_OK)
