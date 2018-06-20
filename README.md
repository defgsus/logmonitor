## Web-view for system logs

Linux/Debian style system logs are parsed to a database and can then be
displayed conveniently in the browser with filtering.

### deployment

```bash
virtualenv -p python3 env
source env/bin/activate
pip install -r requirements.txt

./manage.py migrate
./manage.py createsuperuser
./manage.py runserver
```

The list of logs to parse is located in `logmonitor/settings.py` as `LOG_FILES`
and can be adjusted to your needs.

To get log-files into the database call:
```bash
./manage.py logview_update
```

Cronjobs are supported via [django-kronos](https://github.com/jgorset/django-kronos).
To install the cronjob checkout `logview/cron.py` to adjust scheduled times and then run:
```bash
./manage.py installtasks
```
