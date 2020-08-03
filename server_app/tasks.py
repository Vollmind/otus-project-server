from datetime import datetime, timedelta

from background_task import background
from background_task.models import Task
from django.utils import timezone

from server_app.models import Address

_seconds_between_checks = 10


@background(schedule=_seconds_between_checks)
def update_online_status():
    for address in Address.objects.all():
        address.is_online = (
                timezone.now() - address.last_checked <= timedelta(seconds=_seconds_between_checks)
        )
        address.save()


def start_update_status():
    Task.objects.filter(verbose_name='update_online_status').delete()
    update_online_status(repeat=_seconds_between_checks, verbose_name='update_online_status')