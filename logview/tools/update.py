
from django.conf import settings
from django.db import transaction

from logview.models import LogFileEntry
from .logfiles import load_logfiles


def update_all_log_entries():
    for file_id in settings.LOG_FILES:
        update_log_entries(file_id)


def update_log_entries(file_id):
    filename = settings.LOG_FILES[file_id]

    after_date = None
    qset = LogFileEntry.objects.filter(file=file_id).order_by("-date", "-time")
    if qset.exists():
        after_date = qset[0].datetime()

    data = load_logfiles(filename, file_id, after_date=after_date)

    with transaction.atomic():
        for e in data:
            LogFileEntry.objects.create(
                file=file_id,
                date=e["date"].date(),
                time=e["date"].time(),
                user=e["user"],
                task=e["task"],
                text=e["text"],
                source_ip=e["source_ip"],
            )
