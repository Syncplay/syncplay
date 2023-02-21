
import ast
import datetime
import hashlib
import itertools
import random
import os
import platform
import re
import string
import subprocess
import sys
import time
import traceback
import unicodedata
import urllib.error
import urllib.parse
import urllib.request

from syncplay import constants
from syncplay.messages import getMessage

folderSearchEnabled = True


def isWindows():
    return sys.platform.startswith(constants.OS_WINDOWS)


def isLinux():
    return sys.platform.startswith(constants.OS_LINUX)


def isMacOS():
    return sys.platform.startswith(constants.OS_MACOS)


def isBSD():
    return constants.OS_BSD in sys.platform or sys.platform.startswith(constants.OS_DRAGONFLY)


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
                    # try_one_last_time = False
                    return f(*args, **kwargs)
                    break
                except ExceptionToCheck as e:
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
    for (name, param) in parts.items():
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


def formatSize(numOfBytes, precise=False):
    if numOfBytes == 0:  # E.g. when file size privacy is enabled
        return "???"
    try:
        megabytes = int(numOfBytes) / 1048576.0  # Technically this is a mebibyte, but whatever
        if precise:
            megabytes = round(megabytes, 1)
        else:
            megabytes = int(megabytes)
        return str(megabytes) + getMessage("megabyte-suffix")
    except:  # E.g. when filesize is hashed
        return "???"


def isASCII(s):
    return all(ord(c) < 128 for c in s)


def findResourcePath(resourceName):
    if resourceName == "syncplay.lua":
        resourcePath = os.path.join(findWorkingDir(), "resources", "lua", "intf", resourceName)
    else:
        resourcePath = os.path.join(findWorkingDir(), "resources", resourceName)
    return resourcePath


def findWorkingDir():
    frozen = getattr(sys, 'frozen', '')
    if not frozen:
        path = os.path.dirname(__file__)
    elif frozen in ('dll', 'console_exe', 'windows_exe', 'macosx_app'):
        path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    elif frozen:  # needed for PyInstaller
        if getattr(sys, '_MEIPASS', '') is not None:
            path = getattr(sys, '_MEIPASS', '')  # --onefile
        else:
            path = os.path.dirname(sys.executable)  # --onedir
    else:
        path = ""
    return path


def getResourcesPath():
    if isWindows():
        return findWorkingDir() + "\\resources\\"
    else:
        return findWorkingDir() + "/resources/"


resourcespath = getResourcesPath()
posixresourcespath = findWorkingDir().replace("\\", "/") + "/resources/"


def getDefaultMonospaceFont():
    return constants.MONOSPACE_FONT


def limitedPowerset(s, minLength):
    return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s), minLength, -1))


def blackholeStdoutForFrozenWindow():
    if getattr(sys, 'frozen', '') == "windows_exe":
        class Stderr(object):
            softspace = 0
            _file = None
            _error = None

            def write(self, text, fname='.syncplay.log'):
                if self._file is None and self._error is None:
                    if os.name != 'nt':
                        path = os.path.join(os.getenv('HOME', '.'), fname)
                    else:
                        path = os.path.join(os.getenv('APPDATA', '.'), fname)
                    self._file = open(path, 'a', encoding='utf-8')
                    # TODO: Handle errors.
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


def truncateText(unicodeText, maxLength):
    try:
        unicodeText = unicodeText.decode('utf-8')
    except:
        pass

    try:
        return str(unicodeText.encode("utf-8"), "utf-8", errors="ignore")[:maxLength]
    except:
        pass
    return ""


def splitText(unicodeText, maxLength):
    try:
        unicodeText = unicodeText.decode('utf-8')
    except:
        pass
    try:
        unicodeText = str(unicodeText.encode("utf-8"), "utf-8", errors="ignore")
        unicodeArray = [unicodeText[i:i + maxLength] for i in range(0, len(unicodeText), maxLength)]
        return(unicodeArray)
    except:
        pass
    return [""]

# Relate to file hashing / difference checking:


def stripfilename(filename, stripURL):
    if filename:
        try:
            filename = filename
        except UnicodeDecodeError:
            pass
        filename = urllib.parse.unquote(filename)
        if stripURL:
            try:
                filename = urllib.parse.unquote(filename.split("/")[-1])
            except UnicodeDecodeError:
                filename = urllib.parse.unquote(filename.split("/")[-1])
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


def hashFilename(filename, stripURL=False):
    if isURL(filename):
        stripURL = True
    strippedFilename = stripfilename(filename, stripURL)
    try:
        strippedFilename = strippedFilename.encode('utf-8')
    except UnicodeDecodeError:
        pass
    filenameHash = hashlib.sha256(strippedFilename).hexdigest()[:12]
    return filenameHash


def hashFilesize(size):
    return hashlib.sha256(str(size).encode('utf-8')).hexdigest()[:12]


def sameHashed(string1raw, string1hashed, string2raw, string2hashed):
    try:
        if string1raw.lower() == string2raw.lower():
            return True
    except AttributeError:
        pass
    if string1raw == string2raw:
        return True
    elif string1raw == string2hashed:
        return True
    elif string1hashed == string2raw:
        return True
    elif string1hashed == string2hashed:
        return True


def sameFilename(filename1, filename2):
    try:
        filename1 = filename1
    except UnicodeDecodeError:
        pass
    try:
        filename2 = filename2
    except UnicodeDecodeError:
        pass
    stripURL = True if isURL(filename1) ^ isURL(filename2) else False
    if filename1 == constants.PRIVACY_HIDDENFILENAME or filename2 == constants.PRIVACY_HIDDENFILENAME:
        return True
    elif sameHashed(stripfilename(filename1, stripURL), hashFilename(filename1, stripURL), stripfilename(filename2, stripURL), hashFilename(filename2, stripURL)):
        return True
    else:
        return False


def sameFilesize(filesize1, filesize2):
    if filesize1 == 0 or filesize2 == 0:
        return True
    elif sameHashed(filesize1, hashFilesize(filesize1), filesize2, hashFilesize(filesize2)):
        return True
    else:
        return False


def sameFileduration(duration1, duration2):
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


def isURL(path):
    if path is None:
        return False
    elif "://" in path:
        return True
    else:
        return False


def getPlayerArgumentsByPathAsArray(arguments, path):
    if arguments and not isinstance(arguments, str) and path in arguments:
        return arguments[path]
    else:
        return None


def getPlayerArgumentsByPathAsText(arguments, path):
    argsToReturn = getPlayerArgumentsByPathAsArray(arguments, path)
    return " ".join(argsToReturn) if argsToReturn else ""


def getListAsMultilineString(pathArray):
    return "\n".join(pathArray) if pathArray else ""


def convertMultilineStringToList(multilineString):
    return str.split(multilineString, "\n") if multilineString else []


def playlistIsValid(files):
    if len(files) > constants.PLAYLIST_MAX_ITEMS:
        return False
    elif sum(map(len, files)) > constants.PLAYLIST_MAX_CHARACTERS:
        return False
    return True


def getDomainFromURL(URL):
    try:
        o = urllib.parse.urlparse(URL)
    except ValueError:
        # not a URL
        return None
    if o.hostname is not None and o.hostname.startswith("www."):
        return o.hostname[4:]
    else:
        # may return None if URL does not have domain (invalid url)
        return o.hostname


def open_system_file_browser(path):
    if isURL(path):
        return
    path = os.path.dirname(path)
    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])

def playerPathExists(path):
    if os.path.isfile(path):
        return True
    elif "mpvnet.exe" in path and os.path.isfile(path.replace("mpvnet.exe","mpvnet.com")):
        return True
    else:
        return False

def getListOfPublicServers():
    try:
        import urllib.request, urllib.parse, urllib.error, syncplay, sys
        params = urllib.parse.urlencode({'version': syncplay.version, 'milestone': syncplay.milestone, 'release_number': syncplay.release_number, 'language': syncplay.messages.messages["CURRENT"]})
        if isMacOS():
            import requests
            response = requests.get(constants.SYNCPLAY_PUBLIC_SERVER_LIST_URL.format(params))
            response = response.text
        else:
            f = urllib.request.urlopen(constants.SYNCPLAY_PUBLIC_SERVER_LIST_URL.format(params))
            response = f.read()
            response = response.decode('utf-8')
        response = response.replace("<p>", "").replace("</p>", "").replace("<br />", "").replace("&#8220;", "'").replace("&#8221;", "'").replace(":&#8217;", "'").replace("&#8217;", "'").replace("&#8242;", "'").replace("\n", "").replace("\r", "")  # Fix Wordpress
        response = ast.literal_eval(response)

        if response:
            return response
        else:
            raise IOError
    except:
        if constants.DEBUG_MODE == True:
            traceback.print_exc()
            raise
        else:
            raise IOError(getMessage("failed-to-load-server-list-error"))


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
        salt = salt.encode('utf8')
        password = password.encode('utf8')
        salt = hashlib.sha256(salt).hexdigest().encode('utf8')
        provisionalHash = hashlib.sha256(roomName + salt).hexdigest().encode('utf8')
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
        return ''.join(random.choice(string.ascii_uppercase) for _ in range(quantity))

    @staticmethod
    def _get_random_numbers(quantity):
        return ''.join(random.choice(string.digits) for _ in range(quantity))


class NotControlledRoom(Exception):
    pass
