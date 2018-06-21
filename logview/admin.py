from django.contrib import admin

from .models import LogFileEntry


class LogFileEntryAdmin(admin.ModelAdmin):
    exclude=[]
    model=LogFileEntry
    list_display = (
        "__str__", "time", "date", "source_ip", "user", "task",
    )


admin.site.register(LogFileEntry, LogFileEntryAdmin)
