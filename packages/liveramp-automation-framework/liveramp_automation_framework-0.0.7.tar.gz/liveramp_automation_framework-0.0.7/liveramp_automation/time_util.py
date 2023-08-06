import time
from datetime import date, timedelta, datetime

MACROS = {
    "yesterday": (date.today() - timedelta(days=1)).strftime("%Y%m%d"),
    "today": date.today().strftime("%Y%m%d"),
    "dayOfYear": (date.today().timetuple()).tm_yday,
    "now": datetime.now().strftime("%Y%m%d%H%M%S"),
    "now_format": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "nowconnect": datetime.now().strftime("%Y%m%d-%H%M%S"),  # data ingestion must be in yyyymmdd-hhmmss format
    "three_days_ago": (date.today() - timedelta(days=0)).strftime("%Y%m%d"),
    "two_hours_from_now": (datetime.now() + timedelta(hours=2)).strftime("%Y%m%d-%H%M%S"),
    "24hours_before_now": (datetime.now() - timedelta(hours=24)).strftime("%Y%m%d%H%M%S")
}


def windows_wait(value=3):
    time.sleep(value)
