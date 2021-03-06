import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.html import format_html, mark_safe


class LogFileEntry(models.Model):

    file = models.CharField(verbose_name=_("logfile id"), max_length=32, db_index=True)
    date = models.DateField(verbose_name=_("date"), db_index=True)
    time = models.TimeField(verbose_name=_("time"), db_index=True)
    user = models.CharField(verbose_name=_("user"), max_length=32, db_index=True)
    task = models.CharField(verbose_name=_("task"), max_length=64, db_index=True)
    text = models.TextField(verbose_name=_("text"), db_index=True)

    source_ip = models.GenericIPAddressField(verbose_name=_("source ip"),
                                             null=True, default=None, db_index=True)

    def datetime(self):
        d = self.date
        t = self.time
        return datetime.datetime(d.year, d.month, d.day,
                                 t.hour, t.minute, t.second)

    def source_ip_decorator(self):
        from ..tools.nsmapping import NsMapping
        mapping = NsMapping()
        mapping.do_query = False
        return mark_safe(mapping.ip_decorator(self.source_ip))
    source_ip_decorator.short_description = _("source ip")
    source_ip_decorator.admin_order_field = "source_ip"
