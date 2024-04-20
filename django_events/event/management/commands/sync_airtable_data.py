from django.conf import settings
from django.core.management.base import BaseCommand
from pyairtable import Api

from django_events.event.models import Event


class Command(BaseCommand):
    help = """Sync data between Airtable and Django model
        (Update Django model with Airtable data)
    """

    def handle(self, *args, **options):
        api = Api(settings.AIRTABLE_API_KEY)
        table = api.table(settings.AIRTABLE_BASE_ID, settings.AIRTABLE_TABLE_ID)

        airtable_records = table.all()

        for record in airtable_records:
            airtable_id = record["id"]
            event_name = record["fields"].get("title", "")
            event_date = record["fields"].get("date", "")
            event_created_at = record["fields"].get("created_at", "")
            event_updated_at = record["fields"].get("updated_at", "")
            event_description = record["fields"].get("description", "")

            try:
                event = Event.objects.get(airtable_id=airtable_id)
            except Event.DoesNotExist:
                try:
                    event = Event.objects.get(title=event_name)
                except Event.DoesNotExist:
                    event = Event()

            event.title = event_name
            event.date = event_date
            event.description = event_description
            event.airtable_id = airtable_id
            event.created_at = event_created_at
            event.updated_at = event_updated_at
            event.save()
