from django.conf.urls import url
from . import views


app_name = "honeypot"

urlpatterns = [
    url(r'^(?P<url>.*)/?$',                  views.index_view, name='index'),
    url(r'^(?P<url>.*)\.(?P<file>.*)$',      views.index_view2, name='index2'),
]
