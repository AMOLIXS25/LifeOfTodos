from django.contrib import admin

from .models import TODOO, Reminder

@admin.register(TODOO)
class TODOOAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at',)
    prepopulated_fields = {'slug': ['title']}
    list_filter = ('user', )
    show_facets = admin.ShowFacets.ALWAYS


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ('task', 'user', 'reminder_at', 'sent',)