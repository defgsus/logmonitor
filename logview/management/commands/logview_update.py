# encoding=utf-8
import datetime

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Load all logfiles and populate DB - incrementally!'

    def handle(self, *args, **options):
        starttime = datetime.datetime.now()

        from logview.tools.update import update_task
        update_task()

        endtime = datetime.datetime.now()

        print("TOOK %s" % (endtime - starttime))
