from django.contrib import admin

from apps.training_process.models import Group


@admin.register(Group)
class GroupModelAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'coach',
        'playing_level',
        'training_days',
        'training_time',
    )
