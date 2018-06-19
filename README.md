## Web-view for system logs

### deployment

```bash
virtualenv -p python3 env
source env/bin/activate
pip install -r requirements.txt

./manage.py migrate
./manage.py logview_update
./manage.py createsuperuser
./manage.py runserver
```