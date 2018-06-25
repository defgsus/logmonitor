from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.html import mark_safe


class HoneypotLog(models.Model):

    date = models.DateField(verbose_name=_("date"), db_index=True)
    time = models.TimeField(verbose_name=_("time"), db_index=True)

    source_ip = models.GenericIPAddressField(
        verbose_name=_("source ip"), null=True, default=None, db_index=True)

    url = models.URLField(
        verbose_name=_("url"), max_length=256, db_index=True)
    username = models.CharField(
        verbose_name=_("username"), max_length=48, db_index=True)
    password = models.CharField(
        verbose_name=_("password"), max_length=48, db_index=True)
    params = models.TextField(
        verbose_name=_("parameters"))

    def source_ip_decorator(self):
        from logview.tools.nsmapping import NsMapping
        mapping = NsMapping()
        return mark_safe(mapping.ip_decorator(self.source_ip))
    source_ip_decorator.short_description = _("source ip")
    source_ip_decorator.admin_order_field = "source_ip"
