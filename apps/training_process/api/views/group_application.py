from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from apps.training_process.api.filters import GroupApplicationFilter
from apps.training_process.api.serializers import (
    GroupApplicationRejectSerializer,
    GroupApplicationSerializer,
    GroupApplicationUpdateSerializer,
)
from apps.training_process.models import GroupApplication
from apps.training_process.models.choices import GroupApplicationStatus
from apps.training_process.services import (
    GroupApplicationApproveService,
    GroupApplicationRejectService,
)


class GroupApplicationViewSet(viewsets.ModelViewSet):
    """API для работы с тренировочными группами."""

    queryset = (
        GroupApplication.objects.all()
        .select_related('group__coach__user', 'user')
        .order_by('-id')
    )
    serializer_class = GroupApplicationSerializer
    filterset_class = GroupApplicationFilter
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.action == 'reject':
            return GroupApplicationRejectSerializer
        return super().get_serializer_class()

    def destroy(self, request, *args, **kwargs):
        """
        Удаление заявки на присоединение к группе.

        Удалять можно только заявки в статусе "Новая".
        """

        group_application = self.get_object()
        if not group_application.status == GroupApplicationStatus.NEW:
            raise ValidationError(
                'Удалять можно только заявки в статусе "Новая"'
            )

        self.perform_destroy(group_application)

        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, *args, **kwargs):
        """
        Редактирование заявки на присоединение к группе.

        Редактировать можно только заявки в статусе "Новая".
        """

        group_application = self.get_object()

        # Проверяем, что заявка находится в статусе "Новая"
        if not group_application.status == GroupApplicationStatus.NEW:
            raise ValidationError(
                'Редактировать можно только заявки в статусе "Новая"'
            )

        request_serializer = GroupApplicationUpdateSerializer(
            group_application,
            data=request.data,
            partial=True,
        )
        request_serializer.is_valid(raise_exception=True)
        self.perform_update(request_serializer)

        response_serializer = self.get_serializer(group_application)

        return Response(response_serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary='Отклонение заявки на присоединение к группе',
        request=GroupApplicationRejectSerializer(),
        responses={
            status.HTTP_200_OK: GroupApplicationSerializer,
        },
        parameters=[
            OpenApiParameter(
                name='id',
                type=int,
                location=OpenApiParameter.PATH,
                description='ID отклоняемой заявки',
            ),
        ],
    )
    @action(
        detail=True,
        methods=['POST'],
        url_path='reject',
        url_name='reject',
    )
    def reject(self, request, *args, **kwargs):
        """
        Отклонение заявки на присоединение к тренировочной группе.
        Заявка должна быть в статусе "Новая".
        """

        group_application = self.get_object()
        request_serializer = self.get_serializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        group_application = GroupApplicationRejectService(
            group_application=group_application,
            **request_serializer.validated_data,
        ).execute()

        response_serializer = GroupApplicationSerializer(group_application)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary='Одобрение заявки на присоединение к группе',
        request=None,
        responses={
            status.HTTP_200_OK: GroupApplicationSerializer,
        },
        parameters=[
            OpenApiParameter(
                name='id',
                type=int,
                location=OpenApiParameter.PATH,
                description='ID одобряемой заявки',
            ),
        ],
    )
    @action(
        detail=True,
        methods=['POST'],
        url_path='approve',
        url_name='approve',
    )
    def approve(self, request, *args, **kwargs):
        """
        Одобрение заявки на присоединение к тренировочной группе.
        Заявка должна быть в статусе "Новая".
        """

        group_application = self.get_object()
        group_application = GroupApplicationApproveService(
            group_application=group_application,
        ).execute()

        response_serializer = GroupApplicationSerializer(group_application)
        return Response(response_serializer.data, status=status.HTTP_200_OK)
