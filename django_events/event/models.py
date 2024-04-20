from django.db import models
from django.utils import timezone

from django_events.users.models import User


class EventQuerySet(models.QuerySet):
    def upcoming(self):
        return self.filter(date__gte=timezone.now()).order_by("date")

    def past(self):
        return self.filter(date__lt=timezone.now()).order_by("-date")


class Event(models.Model):
    # event details
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField()

    # event sync metadata
    airtable_id = models.CharField(max_length=100, blank=True)

    # event metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = EventQuerySet.as_manager()

    def __str__(self):
        return self.title


class SubscriptionQuerySet(models.QuerySet):
    def subscribed_upcoming(self):
        return self.filter(event__date__gte=timezone.now()).order_by("event__date")

    def subscribed_past(self):
        return self.filter(event__date__lt=timezone.now()).order_by("-event__date")


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_subscriptions",
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="event_subscriptions",
    )

    objects = SubscriptionQuerySet.as_manager()

    class Meta:
        unique_together = ["user", "event"]

    def __str__(self):
        return f"{self.user} - {self.event}"
