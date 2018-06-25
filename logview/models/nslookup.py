import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _


def linebreaks(text):
    if not text:
        return text
    lines = text.split("\n")
    return "<br/>".join("<nobr>%s</nobr>" % l for l in lines)


class WhoisRequest(models.Model):

    class Meta:
        verbose_name = _("Whois Requests")
        verbose_name_plural = _("Whois Requests")

    date = models.DateTimeField(verbose_name=_("date"))
    ip = models.GenericIPAddressField(verbose_name=_("IP"))
    response = models.TextField(verbose_name=_("response"), null=True, blank=True, default=None)

    def date_decorator(self):
        return "%s" % self.date.replace(microsecond=0)
    date_decorator.short_description = _("date")
    date_decorator.admin_order_field = "date"

    def response_decorator(self):
        return linebreaks(self.response)
    response_decorator.short_description = _("response")
    response_decorator.admin_order_field = "response"
    response_decorator.allow_tags = True


class NslookupRequest(models.Model):

    class Meta:
        verbose_name = _("Nslookup Requests")
        verbose_name_plural = _("Nslookup Requests")

    date = models.DateTimeField(verbose_name=_("date"))
    ip = models.GenericIPAddressField(verbose_name=_("IP"))
    response = models.TextField(verbose_name=_("response"), null=True, blank=True, default=None)

    def date_decorator(self):
        return "%s" % self.date.replace(microsecond=0)
    date_decorator.short_description = _("date")
    date_decorator.admin_order_field = "date"

    def response_decorator(self):
        return linebreaks(self.response)
    response_decorator.short_description = _("response")
    response_decorator.admin_order_field = "response"
    response_decorator.allow_tags = True

