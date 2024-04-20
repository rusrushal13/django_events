from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from django_events.event.models import Event
from django_events.event.models import Subscription

from .serializers import EventsSerializer


class EventViewSet(
    RetrieveModelMixin,
    ListModelMixin,
    UpdateModelMixin,
    GenericViewSet,
    CreateModelMixin,
):
    serializer_class = EventsSerializer
    queryset = Event.objects.all()

    def get_permissions(self):
        if self.action in ["subscribe", "unsubscribe"]:
            if self.request.method in ["POST"]:
                return [IsAuthenticated()]
            return [AllowAny()]
        return super().get_permissions()

    @action(detail=True, methods=["post"])
    def subscribe(self, request, *args, **kwargs):
        event = self.get_object()
        user = request.user

        _, created = Subscription.objects.get_or_create(
            user=user,
            event=event,
        )
        if created:
            return Response(
                {"detail": "Subscribed successfully."},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"detail": "Already subscribed."},
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"])
    def unsubscribe(self, request, *args, **kwargs):
        event = self.get_object()
        user = request.user

        try:
            subscription = Subscription.objects.get(user=user, event=event)
            subscription.delete()
            return Response(
                {"detail": "Unsubscribed successfully."},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Subscription.DoesNotExist:
            return Response(
                {"detail": "Subscription does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )
