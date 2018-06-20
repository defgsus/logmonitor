from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from django.utils.http import urlencode
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .models import *


@login_required
def index_view(request):

    ctx = {
        "page_title": _("Index"),
        "logs": [(key, "%s?file=%s" % (reverse("logview:log"), key))
                 for key in settings.LOG_FILES],
    }

    return render(request, "logview/index.html", ctx)


@login_required
def log_view(request):

    FIELDS = ("file", "date", "user", "task", "text")
    NUM_PER_PAGE = 100

    filters = dict()
    exfilters = dict()
    for name in FIELDS:
        value = request.GET.get("%s0" % name)
        if value:
            filters["%s__icontains" % name] = value
        value = request.GET.get("%s1" % name)
        if value:
            exfilters["%s__icontains" % name] = value

    num_logs_all = LogFileEntry.objects.all().count()

    qset = LogFileEntry.objects.filter(**filters).exclude(**exfilters)
    qset = qset.order_by("-date")

    num_logs = qset.count()

    try:
        cur_page = int(request.GET.get("p", 0))
    except (TypeError, ValueError):
        cur_page = 0
    qset = qset[cur_page*NUM_PER_PAGE:(cur_page+1)*NUM_PER_PAGE]

    num_pages = num_logs // NUM_PER_PAGE

    header_lines = []
    for line in range(2):
        headers = []
        for name in FIELDS:
            value = request.GET.get("%s%s" % (name, line), "")
            headers.append({
                "name": name,
                "widget": """<input type="text" name="%s%s" value="%s" class="table-filter" 
                                    data-ac-url="%s" data-ac-field="%s">""" % (
                    name, line, value,
                    reverse("logview:autocomplete"), name,
                )
            })
        header_lines.append([line, headers])

    def _url(page):
        f = filters.copy()
        f["p"] = page
        url = urlencode(f)
        if not filters:
            url = "?" + url
        return url

    ctx = {
        "page_title": _("Logs"),
        "logs": qset,
        "num_logs": num_logs,
        "num_logs_percent": round(num_logs / max(1, num_logs_all) * 100, 2),
        "headers": FIELDS,
        "header_lines": header_lines,
        "pages": [("""<a href="%s">%s</a>""" % (_url(p), p)) if p!=cur_page else p
                  for p in range(num_pages)],
        "cur_page": cur_page,
        "js": ("logview/autocomplete.js",),
    }

    return render(request, "logview/log.html", ctx)


@login_required
def autocomplete(request):
    field = request.GET.get("n")
    query = request.GET.get("q")
    if not field or not query:
        return JsonResponse({"items":[]})

    filters = {
        "%s__icontains" % field: query,
    }
    qset = LogFileEntry.objects.filter(**filters)
    results = qset.order_by(field).values_list(field).distinct()[:30]
    results = list(r[0] for r in results)

    return JsonResponse({"items":results})
