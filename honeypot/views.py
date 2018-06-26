import os

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.http import HttpResponse
from django.conf import settings

from ipware import get_client_ip

from .models import HoneypotLog


BOB = dict()


def get_bob(ext):
    global BOB
    if ext not in BOB:
        with open(
                os.path.join(settings.BASE_DIR, "honeypot", "templates", "honeypot", "bob.%s" % ext),
                "rb") as fp:
           BOB[ext] = fp.read()
    return BOB[ext]


#@csrf_exempt
#def index_view(request, url):
#    return index_view2(request, url, "")


@csrf_exempt
def index_view(request, url):

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
            url=url,
            username=username or "",
            password=password or "",
            params=parameters,
        )

    if url.lower().endswith(".jpg") or url.lower().endswith(".jpeg"):
        return HttpResponse(get_bob("jpg"), content_type="image/jpeg")

    if url.lower().endswith(".png"):
        return HttpResponse(get_bob("png"), content_type="image/png")

    ctx = {
        "url": url,
        #"file": file,
        "username": username or "",
    }

    if username or password:
        ctx["error"] = "Wrong password or user unknown"

    return render(request, "honeypot/honeypot.html", ctx)
