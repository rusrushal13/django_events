from rest_framework import serializers

from django_events.event.models import Event


class EventsSerializer(serializers.ModelSerializer[Event]):
    class Meta:
        model = Event
        fields = "__all__"

        extra_kwargs = {
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }
