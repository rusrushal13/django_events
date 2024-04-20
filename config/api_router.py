from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from django_events.event.api.views import EventViewSet
from django_events.users.api.views import UserViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)

router.register("event", EventViewSet)

app_name = "api"
urlpatterns = router.urls
