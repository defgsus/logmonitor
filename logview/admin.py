from django.contrib import admin

from .models import *


class LogFileEntryAdmin(admin.ModelAdmin):
    exclude=[]
    model=LogFileEntry
    list_display = (
        "__str__", "time", "date", "source_ip", "user", "task",
    )

admin.site.register(LogFileEntry, LogFileEntryAdmin)


class JobLogAdmin(admin.ModelAdmin):
    exclude=[]
    model=JobLog
    list_display = (
        "__str__", "name", "count", "date_started", "date_finished", "duration", "log_text", "error_text"
    )

admin.site.register(JobLog, JobLogAdmin)


class WhoisRequestAdmin(admin.ModelAdmin):
    exclude=[]
    model=WhoisRequest
    list_display = (
        "__str__", "date", "ip", "response",
    )

admin.site.register(WhoisRequest, WhoisRequestAdmin)


class NslookupRequestAdmin(admin.ModelAdmin):
    exclude=[]
    model=NslookupRequest
    list_display = (
        "__str__", "date", "ip", "response",
    )

admin.site.register(NslookupRequest, NslookupRequestAdmin)