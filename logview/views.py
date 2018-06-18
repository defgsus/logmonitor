from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from django.conf import settings

from .models import *


def index_view(request):

    ctx = {
        "page_title": _("Index"),
        "logs": [(key, "%s?file=%s" % (reverse("logview:log"), key))
                 for key in settings.LOG_FILES],
    }

    return render(request, "logview/index.html", ctx)



def log_view(request):

    FIELDS = ("file", "date", "user", "task", "text")

    filters = dict()
    for name in FIELDS:
        value = request.GET.get(name)
        if value:
            filters["%s__icontains" % name] = value

    num_logs_all = LogFileEntry.objects.all().count()

    qset = LogFileEntry.objects.filter(**filters)
    qset = qset.order_by("-date")

    num_logs = qset.count()
    qset = qset[0:50]

    headers = []
    for name in FIELDS:
        value = request.GET.get(name, "")
        headers.append({
            "name": name,
            "widget": """<input type="text" name="%s" value="%s">""" % (name, value)
        })

    ctx = {
        "page_title": _("logs"),
        "logs": qset,
        "num_logs": num_logs,
        "num_logs_percent": round(num_logs / max(1, num_logs_all) * 100, 2),
        "headers": headers,
    }

    return render(request, "logview/log.html", ctx)

