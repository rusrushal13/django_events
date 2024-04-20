from django.contrib import admin

from django_events.event.models import Event

# Register your models here.


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "description",
        "date",
        "created_at",
        "updated_at",
    ]
    search_fields = ["title", "description"]
    list_filter = ["created_at", "updated_at"]
    date_hierarchy = "date"
    ordering = ["-date"]
    readonly_fields = ["created_at", "updated_at"]
    fieldsets = [
        (None, {"fields": ["title", "description"]}),
        ("Date Information", {"fields": ["date"]}),
        ("Meta Information", {"fields": ["created_at", "updated_at"]}),
    ]
