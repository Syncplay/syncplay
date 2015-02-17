import time
import re
import datetime
from syncplay import constants
from syncplay.messages import getMessage
import sys
import os
import itertools
import hashlib
import random
import string

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
                        msg = getMessage("retrying-notification").format(str(e), mdelay)
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
            if name == "miliseconds":
                time_params["microseconds"] = int(param) * 1000
            else:
                time_params[name] = int(param)
    return datetime.timedelta(**time_params).total_seconds()

def formatTime(timeInSeconds, weeksAsTitles=True):
    if timeInSeconds < 0:
        timeInSeconds = -timeInSeconds
        sign = '-'
    else:
        sign = ''
    timeInSeconds = round(timeInSeconds)
    weeks = timeInSeconds // 604800
    if weeksAsTitles and weeks > 0:
        title = weeks
        weeks = 0
    else:
        title = 0
    days = (timeInSeconds % 604800) // 86400
    hours = (timeInSeconds % 86400) // 3600
    minutes = (timeInSeconds % 3600) // 60
    seconds = timeInSeconds % 60
    if weeks > 0:
        formattedTime = '{0:}{1:.0f}w, {2:.0f}d, {3:02.0f}:{4:02.0f}:{5:02.0f}'.format(sign, weeks, days, hours, minutes, seconds)
    elif days > 0:
        formattedTime = '{0:}{1:.0f}d, {2:02.0f}:{3:02.0f}:{4:02.0f}'.format(sign, days, hours, minutes, seconds)
    elif hours > 0:
        formattedTime = '{0:}{1:02.0f}:{2:02.0f}:{3:02.0f}'.format(sign, hours, minutes, seconds)
    else:
        formattedTime = '{0:}{1:02.0f}:{2:02.0f}'.format(sign, minutes, seconds)
    if title > 0:
        formattedTime = "{0:} (Title {1:.0f})".format(formattedTime, title)
    return formattedTime

def formatSize (bytes, precise=False):
    if bytes == 0: # E.g. when file size privacy is enabled
        return "???"
    try:
        megabytes = int(bytes) / 1048576.0 # Technically this is a mebibyte, but whatever
        if precise:
            megabytes = round(megabytes, 1)
        else:
            megabytes = int(megabytes)
        return str(megabytes) + getMessage("megabyte-suffix")
    except: # E.g. when filesize is hashed
        return "???"

def isASCII(s):
    return all(ord(c) < 128 for c in s)

def findWorkingDir():
    frozen = getattr(sys, 'frozen', '')
    if not frozen:
        path = os.path.dirname(os.path.dirname(__file__))
    elif frozen in ('dll', 'console_exe', 'windows_exe'):
        path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    else:
        path = ""
    return path

def limitedPowerset(s, minLength):
    return itertools.chain.from_iterable(itertools.combinations(s, r) for r in xrange(len(s), minLength, -1))

def blackholeStdoutForFrozenWindow():
    if getattr(sys, 'frozen', '') == "windows_exe":
        class Stderr(object):
            softspace = 0
            _file = None
            _error = None
            def write(self, text, fname='.syncplay.log'):
                if self._file is None and self._error is None:
                    if os.name <> 'nt':
                        path = os.path.join(os.getenv('HOME', '.'), fname)
                    else:
                        path = os.path.join(os.getenv('APPDATA', '.'), fname)
                    self._file = open(path, 'a')
                    #TODO: Handle errors.
                if self._file is not None:
                    self._file.write(text)
                    self._file.flush()
            def flush(self):
                if self._file is not None:
                    self._file.flush()
        sys.stderr = Stderr()
        del Stderr

        class Blackhole(object):
            softspace = 0
            def write(self, text):
                pass
            def flush(self):
                pass
        sys.stdout = Blackhole()
        del Blackhole

# Relate to file hashing / difference checking:

def stripfilename(filename):
    if filename:
        return re.sub(constants.FILENAME_STRIP_REGEX, "", filename)
    else:
        return ""

def stripRoomName(RoomName):
    if RoomName:
        try:
            return re.sub(constants.ROOM_NAME_STRIP_REGEX, "\g<roomnamebase>", RoomName)
        except IndexError:
            return RoomName
    else:
        return ""

def hashFilename(filename):
    return hashlib.sha256(stripfilename(filename).encode('utf-8')).hexdigest()[:12]

def hashFilesize(size):
    return hashlib.sha256(str(size)).hexdigest()[:12]

def sameHashed(string1raw, string1hashed, string2raw, string2hashed):
    if string1raw == string2raw:
        return True
    elif string1raw == string2hashed:
        return True
    elif string1hashed == string2raw:
        return True
    elif string1hashed == string2hashed:
        return True

def sameFilename (filename1, filename2):
    if filename1 == constants.PRIVACY_HIDDENFILENAME or filename2 == constants.PRIVACY_HIDDENFILENAME:
        return True
    elif sameHashed(stripfilename(filename1), hashFilename(filename1), stripfilename(filename2), hashFilename(filename2)):
        return True
    else:
        return False

def sameFilesize (filesize1, filesize2):
    if filesize1 == 0 or filesize2 == 0:
        return True
    elif sameHashed(filesize1, hashFilesize(filesize1), filesize2, hashFilesize(filesize2)):
        return True
    else:
        return False

def sameFileduration (duration1, duration2):
    if not constants.SHOW_DURATION_NOTIFICATION:
        return True
    elif abs(round(duration1) - round(duration2)) < constants.DIFFERENT_DURATION_THRESHOLD:
        return True
    else:
        return False

def meetsMinVersion(version, minVersion):
    def versiontotuple(ver):
        return tuple(map(int, ver.split(".")))
    return versiontotuple(version) >= versiontotuple(minVersion)

class RoomPasswordProvider(object):
    CONTROLLED_ROOM_REGEX = re.compile("^\+(.*):(\w{12})$")
    PASSWORD_REGEX = re.compile("[A-Z]{2}-\d{3}-\d{3}")

    @staticmethod
    def isControlledRoom(roomName):
        return bool(re.match(RoomPasswordProvider.CONTROLLED_ROOM_REGEX, roomName))

    @staticmethod
    def check(roomName, password, salt):
        if not password or not re.match(RoomPasswordProvider.PASSWORD_REGEX, password):
            raise ValueError()

        if not roomName:
            raise NotControlledRoom()
        match = re.match(RoomPasswordProvider.CONTROLLED_ROOM_REGEX, roomName)
        if not match:
            raise NotControlledRoom()
        roomHash = match.group(2)
        computedHash = RoomPasswordProvider._computeRoomHash(match.group(1), password, salt)
        return roomHash == computedHash

    @staticmethod
    def getControlledRoomName(roomName, password, salt):
        return "+" + roomName + ":" + RoomPasswordProvider._computeRoomHash(roomName, password, salt)

    @staticmethod
    def _computeRoomHash(roomName, password, salt):
        roomName = roomName.encode('utf8')
        salt = hashlib.sha256(salt).hexdigest()
        provisionalHash = hashlib.sha256(roomName + salt).hexdigest()
        return hashlib.sha1(provisionalHash + salt + password).hexdigest()[:12].upper()

class RandomStringGenerator(object):
    @staticmethod
    def generate_room_password():
        parts = (
            RandomStringGenerator._get_random_letters(2),
            RandomStringGenerator._get_random_numbers(3),
            RandomStringGenerator._get_random_numbers(3)
        )
        return "{}-{}-{}".format(*parts)

    @staticmethod
    def generate_server_salt():
        parts = (
            RandomStringGenerator._get_random_letters(10),
        )
        return "{}".format(*parts)

    @staticmethod
    def _get_random_letters(quantity):
        return ''.join(random.choice(string.ascii_uppercase) for _ in xrange(quantity))

    @staticmethod
    def _get_random_numbers(quantity):
        return ''.join(random.choice(string.digits) for _ in xrange(quantity))

class NotControlledRoom(Exception):
    pass