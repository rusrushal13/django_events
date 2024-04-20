from django.urls import path

from django_events.event.views import upcoming_events

app_name = "event"

urlpatterns = [
    path("", view=upcoming_events, name="list"),
]
