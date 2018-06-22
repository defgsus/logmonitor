from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from ipware import get_client_ip

from .models import HoneypotLog


@csrf_exempt
def index_view(request, url):
    return index_view2(request, url, "")


@csrf_exempt
def index_view2(request, url, file):

    now = timezone.now()

    if request.method == "POST":
        params = request.POST
    else:
        params = request.GET

    ip, is_routable = get_client_ip(request)

    username = params.get("username")
    password = params.get("password")
    parameters = repr(params)[12:-1]
    if len(parameters) < 3:
        parameters = ""

    if parameters:
        HoneypotLog.objects.create(
            date=now.date(),
            time=now.time(),
            source_ip=ip,
            url=("%s.%s" % (url, file)) if file else url,
            username=username or "",
            password=password or "",
            params=parameters,
        )

    ctx = {
        "url": url,
        "file": file,
        "username": username or "",
    }

    if username or password:
        ctx["error"] = "Wrong password or user unknown"

    return render(request, "honeypot/honeypot.html", ctx)
