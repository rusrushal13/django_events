from django.shortcuts import render

from django_events.event.models import Event


def upcoming_events(request):
    upcoming_events = Event.objects.upcoming()
    user = request.user
    subscribed_events = (
        set(user.user_subscriptions.values_list("event_id", flat=True))
        if user.is_authenticated
        else set()
    )

    event_data = []
    for event in upcoming_events:
        is_subscribed = event.id in subscribed_events
        event_data.append({"event": event, "is_subscribed": is_subscribed})

    return render(
        request,
        "event/upcoming_events.html",
        {
            "event_data": event_data,
            "user": user,
        },
    )
