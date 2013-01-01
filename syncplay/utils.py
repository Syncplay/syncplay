import time
import re
import datetime
from syncplay import constants
from syncplay.messages import getMessage

def retry(ExceptionToCheck, tries=4, delay=3, backoff=2, logger=None):
    """Retry calling the decorated function using an exponential backoff.

    http://www.saltycrane.com/blog/2009/11/trying-out-retry-decorator-python/
    original from: http://wiki.python.org/moin/PythonDecoratorLibrary#Retry

    :param ExceptionToCheck: the exception to check. may be a tuple of
        excpetions to check
    :type ExceptionToCheck: Exception or tuple
    :param tries: number of times to try (not retry) before giving up
    :type tries: int
    :param delay: initial delay between retries in seconds
    :type delay: int
    :param backoff: backoff multiplier e.g. value of 2 will double the delay
        each retry
    :type backoff: int
    :param logger: logger to use. If None, print
    :type logger: logging.Logger instance
    """
    def deco_retry(f):
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            try_one_last_time = True
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                    try_one_last_time = False
                    break
                except ExceptionToCheck, e:
                    if logger:
                        msg = getMessage("en", "retrying-notification") % (str(e), mdelay)
                        logger.warning(msg)
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            if try_one_last_time:
                return f(*args, **kwargs)
            return
        return f_retry  # true decorator
    return deco_retry

def parseTime(timeStr):
    regex = re.compile(constants.PARSE_TIME_REGEX)
    parts = regex.match(timeStr)
    if not parts:
        return
    parts = parts.groupdict()
    time_params = {}
    for (name, param) in parts.iteritems():
        if param:
            if(name == "miliseconds"):
                time_params["microseconds"] = int(param) * 1000
            else:
                time_params[name] = int(param)
    return datetime.timedelta(**time_params).total_seconds()
    
def formatTime(timeInSeconds):
    timeInSeconds = round(timeInSeconds)
    weeks = timeInSeconds // 604800
    days = (timeInSeconds % 604800) // 86400
    hours = (timeInSeconds % 86400) // 3600
    minutes = (timeInSeconds % 3600) // 60
    seconds = timeInSeconds % 60
    if(weeks > 0):
        return '{0:.0f}w, {1:.0f}d, {2:02.0f}:{3:02.0f}:{4:02.0f}'.format(weeks, days, hours, minutes, seconds)
    elif(days > 0):
        return '{0:.0f}d, {1:02.0f}:{2:02.0f}:{3:02.0f}'.format(days, hours, minutes, seconds)
    elif(hours > 0):
        return '{0:02.0f}:{1:02.0f}:{2:02.0f}'.format(hours, minutes, seconds)
    else:
        return '{0:02.0f}:{1:02.0f}'.format(minutes, seconds)
