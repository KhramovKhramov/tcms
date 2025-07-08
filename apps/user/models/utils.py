from django.db.models import Func, IntegerField


class YearsBetween(Func):
    """
    Для подсчета кол-ва полных лет между датами
    в аннотациях на уровне SQL.
    """

    function = 'DATE_PART'
    template = "%(function)s('year', AGE(%(expressions)s))::int"
    output_field = IntegerField()
