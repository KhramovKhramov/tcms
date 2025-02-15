from django.db.models import Case, CharField, F, Q, Value, When
from django.db.models.functions import Concat


def get_user_full_name_annotation(
    user_lookup: str, field='full_name'
) -> dict[str, Concat]:
    """
    Создание аннотации 'full_name' с ФИО пользователя,
    создаваемой из полей last_name, first_name и patronymic модели User.

    :param user_lookup: Путь до объекта модели пользователя.
    :param field: Наименования аннотированного поля.
    """

    return {
        field: Concat(
            F(f'{user_lookup}last_name'),
            Value(' '),
            F(f'{user_lookup}first_name'),
            Case(
                When(
                    Q(**{f'{user_lookup}patronymic__isnull': True})
                    | Q(**{f'{user_lookup}patronymic': ''}),
                    then=Value(''),
                ),
                default=Concat(
                    Value(' '),
                    F(f'{user_lookup}patronymic'),
                ),
            ),
            output_field=CharField(),
        )
    }
