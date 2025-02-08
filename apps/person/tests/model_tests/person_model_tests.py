import pytest

from apps.person.tests.factories.person import PersonFactory

class TestPersonModel:
    """Тесты модели пользователя."""

    @pytest.mark.django_db
    def test_full_name(self):
        """Проверка работы вычисляемого поля с ФИО пользователя."""

        persons = PersonFactory.create_batch(2)
        another_person = PersonFactory.create(
            patronymic='Ивановна',
        )

        for person in [*persons, another_person]:
            full_name = (
                f'{person.last_name} {person.first_name} {person.patronymic or ""}'
            )

            assert person.full_name == full_name.strip()
