import datetime

import pytz


def seconds_until(hours, minutes):
    eastern_timezone = pytz.timezone('US/Eastern')

    now = datetime.datetime.now(eastern_timezone)

    # Create a datetime object for the given time in the Eastern Timezone
    given_time = datetime.time(hours, minutes)
    future_exec = eastern_timezone.localize(datetime.datetime.combine(now, given_time))

    # If the given time is before the current time, add one day to the future execution time
    if future_exec < now:
        future_exec += datetime.timedelta(days=1)

    # Calculate the time difference in seconds
    seconds_until_execution = (future_exec - now).total_seconds()

    return seconds_until_execution