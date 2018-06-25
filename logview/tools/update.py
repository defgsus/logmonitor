
from django.conf import settings
from django.db import transaction

from logview.models import LogFileEntry, Logger
from .logfiles import load_logfiles, parse_entry


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


def parse_ips():
    with transaction.atomic():
        for log in LogFileEntry.objects.filter(source_ip=None):
            fields = {
                "user": log.user,
                "task": log.task,
                "text": log.text,
            }
            fields = parse_entry(fields)
            if fields.get("source_ip"):
                log.source_ip = fields["source_ip"]
                log.save()


def get_nslookups():
    from .nslookup import get_nslookup, get_whois
    ips = LogFileEntry.objects.all().exclude(source_ip=None).values_list("source_ip").distinct()
    ips = set(v[0] for v in ips)

    for ip in ips:
        get_nslookup(ip)
        get_whois(ip)
