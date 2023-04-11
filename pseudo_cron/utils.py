import datetime

import pytz
from django.conf import settings
from django.utils.timezone import make_aware


def timestamp_to_datetime(ts: int):
    return make_aware(
        datetime.datetime.fromtimestamp(ts),
        pytz.timezone(settings.TIME_ZONE)
    )
