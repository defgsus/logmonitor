from django.conf.urls import url
from . import views


app_name = "logview"

urlpatterns = [
    url(r'^index/?$',                    views.index_view, name='index_view'),
]
