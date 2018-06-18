from django.conf.urls import url
from . import views


app_name = "logview"

urlpatterns = [
    url(r'^index/?$',                       views.index_view, name='index'),
    url(r'^logs/?$',                        views.log_view, name='log'),

    url(r'^ac/?$',                          views.autocomplete, name='autocomplete'),
]
