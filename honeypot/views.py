from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from ipware import get_client_ip


@csrf_exempt
def index_view(request, url):
    return index_view2(url, "")


@csrf_exempt
def index_view2(request, url, file):

    if request.method == "POST":
        params = request.POST
    else:
        params = request.GET

    ip, is_routable = get_client_ip(request)

    username = params.get("username")
    password = params.get("password")

    ctx = {
        "url": url,
        "file": file,
        "username": username or "",
    }

    if username or password:
        ctx["error"] = "Wrong password or user unknown"

    return render(request, "honeypot/honeypot.html", ctx)
