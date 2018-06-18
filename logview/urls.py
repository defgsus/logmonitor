from django.conf.urls import url
from . import views


app_name = "logview"

urlpatterns = [
    url(r'^index/?$',                       views.index_view, name='index'),
    url(r'^logs/(?P<log_name>[a-z]+)/?$',       views.log_view, name='log'),
]
