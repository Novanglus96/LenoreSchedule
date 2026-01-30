import pytest
from ninja.testing import TestClient
from backend.api import api
import pytz
import os
from django.utils import timezone


def current_date():
    today = timezone.now()
    tz_timezone = pytz.timezone(os.environ.get("TIMEZONE"))
    today_tz = today.astimezone(tz_timezone).date()
    return today_tz


@pytest.fixture(scope="session")
def api_client():
    return TestClient(api)


@pytest.fixture()
def today_date():
    return current_date()
