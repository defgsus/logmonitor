
import kronos

# see https://github.com/jgorset/django-kronos


@kronos.register("0 * * * *")
def logview_update():
    """
    Read logs into database
    """
    from logview.tools.update import update_task
    update_task()

