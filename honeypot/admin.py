from django.contrib import admin

from .models import HoneypotLog


class HoneypotLogAdmin(admin.ModelAdmin):
    exclude=[]
    model=HoneypotLog
    list_display = (
        "__str__", "time", "date", "source_ip_decorator", "url", "username", "password", "params",
    )


admin.site.register(HoneypotLog, HoneypotLogAdmin)
