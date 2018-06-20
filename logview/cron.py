
import kronos

# see https://github.com/jgorset/django-kronos


@kronos.register("0 2,6,10,14,18,22 * * *")
def logview_update():
    """
    Read logs into database
    """
    from logview.tools.update import update_all_log_entries
    update_all_log_entries()

