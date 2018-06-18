from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from django.utils.http import urlencode
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
    NUM_PER_PAGE = 100

    filters = dict()
    for name in FIELDS:
        value = request.GET.get(name)
        if value:
            filters["%s__icontains" % name] = value

    num_logs_all = LogFileEntry.objects.all().count()

    qset = LogFileEntry.objects.filter(**filters)
    qset = qset.order_by("-date")

    num_logs = qset.count()

    try:
        cur_page = int(request.GET.get("p", 0))
    except (TypeError, ValueError):
        cur_page = 0
    qset = qset[cur_page*NUM_PER_PAGE:(cur_page+1)*NUM_PER_PAGE]

    num_pages = num_logs // NUM_PER_PAGE

    headers = []
    for name in FIELDS:
        value = request.GET.get(name, "")
        headers.append({
            "name": name,
            "widget": """<input type="text" name="%s" value="%s">""" % (name, value)
        })

    def _url(page):
        f = filters.copy()
        f["p"] = page
        url = urlencode(f)
        if not filters:
            url = "?" + url
        return url

    ctx = {
        "page_title": _("logs"),
        "logs": qset,
        "num_logs": num_logs,
        "num_logs_percent": round(num_logs / max(1, num_logs_all) * 100, 2),
        "headers": headers,
        "pages": [(p, """<a href="%s">%s</a>""" % (_url(p), p))
                  for p in range(num_pages)],
        "cur_page": cur_page,
    }

    return render(request, "logview/log.html", ctx)

