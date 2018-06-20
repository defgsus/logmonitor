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

    FIELDS = ("file", "date", "time", "user", "task", "text")
    NUM_PER_PAGE = 1000

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

    queries = {key: request.GET[key] for key in request.GET if request.GET[key]}
    paginator = paginator_markup(qset, queries, cur_page, NUM_PER_PAGE)
    histogram = histogram_markup(qset, queries)

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

    ctx = {
        "page_title": _("Logs"),
        "logs": qset,
        "num_logs": num_logs,
        "num_logs_percent": round(num_logs / max(1, num_logs_all) * 100, 2),
        "headers": FIELDS,
        "header_lines": header_lines,
        "paginator": paginator,
        "histogram": histogram,
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


def paginator_markup(qset, filters, cur_page, NUM_PER_PAGE):
    num_pages = qset.count() // NUM_PER_PAGE

    def _url(page):
        f = filters.copy()
        f["p"] = page
        url = urlencode(f)
        if f:
            url = "?" + url
        return url

    log_dates = [datetime.datetime(v[0].year, v[0].month, v[0].day, v[1].hour, v[1].minute, v[1].second)
                 for v in qset.order_by("-date").values_list("date", "time")]

    date_histogram = dict()
    for i, date in enumerate(log_dates):
        key = i // NUM_PER_PAGE
        if key not in date_histogram:
            date_histogram[key] = []
        date_histogram[key].append(date)
    for key in date_histogram:
        h = sorted(date_histogram[key])
        if len(h) == 1:
            tip = "%s" % h[0]
        else:
            h1, h2 = h[0], h[-1]
            if h1.date() == h2.date():
                tip = "%s, %s - %s" % (h1.date(), h1.time(), h2.time())
            else:
                tip = "%s - %s" % (h1.date(), h2.date())
        date_histogram[key] = {
            "page": key,
            "tip": tip,
            "url": _url(key),
            "class": "bold" if cur_page == key else "",
        }

    markup = """<div class="paginator">"""

    for page in date_histogram:
        h = date_histogram[page]
        markup += """<a href="%(url)s" class="%(class)s" title="%(tip)s">%(page)s</a>""" % h

    markup += """</div>"""
    return markup


def histogram_markup(qset, filters):
    log_dates = [datetime.datetime(v[0].year, v[0].month, v[0].day, v[1].hour, v[1].minute, v[1].second)
                 for v in qset.order_by("date").values_list("date", "time")]

    min_ord, max_ord = log_dates[0].toordinal(), log_dates[-1].toordinal()
    num_per_bin = max(1, (max_ord - min_ord) // 100)

    date_histogram = {i//num_per_bin: []
                      for i in range(0, max_ord-min_ord)}

    for i, date in enumerate(log_dates):
        o = date.toordinal() - min_ord
        key = o // num_per_bin
        if key not in date_histogram:
            date_histogram[key] = []
        date_histogram[key].append(date)
    for key in date_histogram:
        h = sorted(date_histogram[key])
        if len(h) == 0:
            tip = "%s - %s" % (
                datetime.date.fromordinal(key * num_per_bin + min_ord),
                datetime.date.fromordinal((key * num_per_bin+num_per_bin-1) + min_ord)
            )
        elif len(h) == 1:
            tip = "%s" % h[0]
        else:
            h1, h2 = h[0], h[-1]
            if h1.date() == h2.date():
                tip = "%s, %s - %s" % (h1.date(), h1.time(), h2.time())
            else:
                tip = "%s - %s" % (h1.date(), h2.date())
        tip = "%s matches, %s" % (len(h), tip)
        date_histogram[key] = {
            "count": len(h),
            "tip": tip
        }
    max_count = max(1, max(h["count"] for h in date_histogram.values()))
    for key in date_histogram:
        h = date_histogram[key]
        h["percent"] = round(h["count"] / max_count * 100, 1)

    markup = """<div class="histogram">"""

    for page in date_histogram:
        h = date_histogram[page]
        markup += """<div class="column" title="%(tip)s">
        <div class="value" style="height:%(percent)s%%"></div></div>""" % h

    markup += """</div>"""
    return markup