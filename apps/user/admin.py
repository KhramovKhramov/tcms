from django.contrib import admin

from apps.user.models import Administrator, Coach, User


@admin.register(User)
class UserModelAdmin(admin.ModelAdmin):
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


@admin.register(Administrator)
class AdministratorModelAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'date_from',
        'date_to',
    )


@admin.register(Coach)
class CoachModelAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'date_from',
        'date_to',
        'position',
    )
