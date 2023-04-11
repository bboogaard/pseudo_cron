# pseudo-cron

Pseudo Cron Middleware for Django

## Rationale

Schedule tasks for periodic execution without crontab.

## Support

Supports: Python 3.9.

Supports Django Versions: 3.2.

## Installation

```shell
$ pip install pseudo_cron
```

## Usage

Add `pseudo_cron` to `INSTALLED_APPS`.

Run migrations:

```python
python manage.py migrate
```

Add the middleware:

```python
MIDDLEWARE = [
    ...,
    'pseudo_cron.middleware.CronMiddleware'
]
```

Add a `cron.py` module to your app and schedule your periodic task:

```python
from pseudo_cron.decorators import schedule_job


@schedule_job(24 * 60 * 60)  # Run every 24 hrs
def my_task():
    ...
```