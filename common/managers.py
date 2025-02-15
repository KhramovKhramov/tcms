from abc import ABC, abstractmethod

from common.utils import get_user_full_name_annotation


class UserFullNameAnnotationMixin(ABC):
    """
    Абстрактный класс, добавляющий возможность с помощью метода
    with_full_name_annotation добавить к кверисету аннотированную строку с
    полным именем пользователя.

    Для корректной работы необходимо добавить к классу-наследнику аттрибут
    user_field_name с путем до поля user.
    """

    @property
    @abstractmethod
    def user_field_name(self):
        raise NotImplementedError()

    def with_full_name_annotation(self):
        """Добавляет к кверисету аннотацию с ФИО пользователя."""

        field_name = self.user_field_name
        user_lookup = '' if not field_name else f'{field_name}__'

        return self.annotate(**get_user_full_name_annotation(user_lookup))
