from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from django.conf import settings


def index_view(request):

    ctx = {
        "page_title": _("Index"),
        "logs": [(key, reverse("logview:log", args=(key,))) for key in settings.LOG_FILES],
    }

    return render(request, "logview/index.html", ctx)



def log_view(request, log_name):

    ctx = {
        "page_title": log_name,
        "log_name": log_name,
    }

    return render(request, "logview/log.html", ctx)

