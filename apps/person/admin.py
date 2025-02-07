from django.contrib import admin

from apps.person.models import Person


@admin.register(Person)
class PersonModelAdmin(admin.ModelAdmin):
    list_display = (
        'get_full_name',
        'email',
        'phone',
        'date_of_birth',
        'gender',
    )

    def get_full_name(self, obj):
        return obj.full_name

    get_full_name.short_description = 'ФИО'
