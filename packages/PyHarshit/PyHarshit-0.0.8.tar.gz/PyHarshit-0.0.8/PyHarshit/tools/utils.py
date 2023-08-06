import time, asyncio, pytz, datetime
from datetime import datetime
import urllib
from urllib.request import urlopen



def tGap(t):
    time.sleep(t)

def aGap(t):
    asyncio.sleep(t)

def currentTime():
    now = datetime.now()
    currenttime = now.strftime("%H:%M:%S")
    return currenttime

def _m(timezone):
    chennai_tz = pytz.timezone(timezone)
    now = datetime.datetime.now(chennai_tz)
    am_pm = now.strftime("%p")
    return am_pm

def zoneTime(timezone):
    tz = pytz.timezone(timezone)
    current_time = datetime.now(tz)
    time_12hr_format = current_time.strftime("%I:%M:%S %p")
    return time_12hr_format



def internet_available():
    """
    Query internet using python
    :return:
    """
    try:
        urlopen('https://www.google.com', timeout=1)
        return True
    except urllib.error.URLError as Error:
        print(Error)
        return False
