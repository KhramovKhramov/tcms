from django.contrib import admin

from apps.training_process.models import Group, GroupApplication


@admin.register(Group)
class GroupModelAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'coach',
        'playing_level',
        'training_days',
        'training_time',
    )


@admin.register(GroupApplication)
class GroupApplicationModelAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'group',
        'created_at',
        'status',
        'playing_level',
        'comment',
    )
