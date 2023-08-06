# Django Master data
0. install dsm-django-masterdata
```
pip install pip install dsm-django-masterdata
```
1. install django app in `settings.py`
```python
INSTALLED_APPS = [
    ...
    'dsm_django_masterdata.hscode',
    'dsm_django_masterdata.area',
    ...
]
```

2. migrate database
```
python manage.py migrate
```

3. check data in admin page

## How to use
- HScode
```python
from dsm_django_masterdata.hscode.models import HScode
hs_code = HScode.objects.all()
```
- Area
```python
from dsm_django_masterdata.area.models import Area
area = Area.objects.all()
```