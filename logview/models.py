from django.db import models
from django.utils.translation import ugettext_lazy as _


class LogFileEntry(models.Model):

    file = models.CharField(verbose_name=_("logfile id"), max_length=32, db_index=True)
    date = models.DateTimeField(verbose_name=_("date"), db_index=True)
    user = models.CharField(verbose_name=_("user"), max_length=32, db_index=True)
    task = models.CharField(verbose_name=_("task"), max_length=64, db_index=True)
    text = models.TextField(verbose_name=_("text"), db_index=True)
