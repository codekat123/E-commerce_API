from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from ..models import Notification


@shared_task(
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3},
)
def delete_old_notifications():

    cutoff = timezone.now() - timedelta(days=10)

    BATCH_SIZE = 1000

    while True:
        ids = list(
            Notification.objects
            .filter(
                is_read=True,
                created_at__lt=cutoff,
            )
            .values_list("id", flat=True)[:BATCH_SIZE]
        )

        if not ids:
            break

        Notification.objects.filter(id__in=ids).delete()