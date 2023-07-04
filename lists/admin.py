from django.contrib import admin

from .models import List, ListItem


class ListItemInline(admin.TabularInline):
    model = ListItem


class ListAdmin(admin.ModelAdmin):
    inlines = [
        ListItemInline,
    ]


admin.site.register(List, ListAdmin)
