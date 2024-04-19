from datetime import datetime, timezone
from pytz import timezone as pyzt_timezone

class TimeStamper:
    def __init__(self, timezone="Europe/Prague"):
        self.timezone = timezone

    def setTimezone(self, newTimezone):
        self.timezone = newTimezone

    def initTimezone(self):
        # get UTC time
        utc_time = datetime.now(timezone.utc)
        # init pytz timezone
        tz = pyzt_timezone(self.timezone)
        # get timezone time
        tz_time = utc_time.astimezone(tz)

        return tz_time
    
    def getTimeStamp(self):
        tz_time = self.initTimezone()
        timestamp = f"{tz_time.hour:02d}:{tz_time.minute:02d}:{tz_time.second:02d}"

        return timestamp
    
    def getDateStamp(self):
        tz_time = self.initTimezone()
        datestamp = f"{tz_time.year}-{tz_time.month:02d}-{tz_time.day:02d}"

        return datestamp
    
    def getDateTimeStamp(self):
        tz_time = self.initTimezone()
        datetimestamp = f"{self.getDateStamp()} {self.getTimeStamp()}"

        return datetimestamp

        

