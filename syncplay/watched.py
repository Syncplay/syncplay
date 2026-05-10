# coding:utf8

"""
Watched episode and playlist warning helpers.

This module contains client-side helpers for watched episode tracking,
watched-subfolder lookup, episode filename parsing, and skipped/out-of-sequence
playlist warnings. It does not modify shared playlist state or room playstate.
"""

import datetime
import json
import os
import re
import shutil
import time

from syncplay import constants, utils
from syncplay.messages import getMessage


class EpisodeFilenameParser(object):
    """Parse episode numbers from filenames using single-file and contextual heuristics."""

    def getContext(self, contextFilenames):
        if not contextFilenames:
            return None
        return {"scores": self._getEpisodeFilenameContextScores(contextFilenames)}

    def parse(self, filename, contextFilenames=None, context=None):
        if not filename:
            return None

        baseName = os.path.basename(filename)
        cleanedName = self._normaliseEpisodeFilename(baseName)
        if not cleanedName:
            return None

        candidates = self._getEpisodeFilenameCandidatesFromCleanedName(cleanedName)
        if not candidates:
            return None

        if context is None and contextFilenames:
            context = self.getContext(contextFilenames)
        contextScores = context.get("scores") if context else None

        candidate = self._chooseEpisodeFilenameCandidate(candidates, contextScores)
        if not candidate:
            return None
        return self._episodeCandidateToInfo(candidate)

    def _episodeCandidateToInfo(self, candidate):
        return {
            "seriesKey": candidate.get("seriesKey"),
            "season": candidate.get("season"),
            "episodeStart": candidate.get("episodeStart"),
            "episodeEnd": candidate.get("episodeEnd"),
        }

    def _getEpisodeFilenameCandidatesFromCleanedName(self, cleanedName):
        candidates = []

        explicitPatterns = [
            (120, "seasonEpisode", re.compile(r'(?i)(?P<prefix>.*?)[\s._-]*S(?P<season>\d{1,2})[\s._-]*E(?P<episode>\d{1,3}(?:\.5)?)(?:\s*(?:-|\+)\s*E?(?P<episodeEnd>\d{1,3}(?:\.5)?))?(?P<suffix>(?:[\s._-].*)?)$')),
            (115, "seasonEpisode", re.compile(r'(?i)(?P<prefix>.*?)[\s._-]+(?P<season>\d{1,2})x(?P<episode>\d{1,3}(?:\.5)?)(?:\s*(?:-|\+)\s*(?P<episodeEnd>\d{1,3}(?:\.5)?))?(?P<suffix>(?:[\s._-].*)?)$')),
            (105, "episodeWord", re.compile(r'(?i)(?P<prefix>.*?)[\s._-]+(?:episode|ep|e)[\s._-]*(?P<episode>\d{1,3}(?:\.5)?)(?:\s*(?:-|\+)\s*(?P<episodeEnd>\d{1,3}(?:\.5)?))?(?P<suffix>(?:[\s._-].*)?)$')),
        ]

        for baseScore, candidateType, pattern in explicitPatterns:
            match = pattern.match(cleanedName)
            if match:
                self._addEpisodeFilenameCandidateFromMatch(candidates, match, baseScore, candidateType, True)

        self._addNumericEpisodeFilenameCandidates(candidates, cleanedName)
        return candidates

    def _parseEpisodeNumberToken(self, episodeToken):
        # Only .5 fractional episodes are supported; halves compare safely as floats.
        if episodeToken.endswith('.5'):
            return int(episodeToken[:-2]) + 0.5
        return int(episodeToken)

    def _addEpisodeFilenameCandidateFromMatch(self, candidates, match, baseScore, candidateType, explicit):
        groups = match.groupdict()
        episodeToken = groups.get('episode')
        if not episodeToken:
            return

        episode = self._parseEpisodeNumberToken(episodeToken)
        episodeEndText = groups.get('episodeEnd')
        episodeEnd = self._parseEpisodeNumberToken(episodeEndText) if episodeEndText else None
        season = groups.get('season')
        self._addEpisodeFilenameCandidateFromParts(
            candidates,
            groups.get('prefix') or "",
            groups.get('suffix') or "",
            episode,
            episodeEnd,
            episodeToken,
            baseScore,
            candidateType,
            explicit,
            int(season) if season else None,
        )

    def _addNumericEpisodeFilenameCandidates(self, candidates, cleanedName):
        numberPattern = re.compile(r'(?<![A-Za-z0-9.])(?P<episode>\d{1,3}(?:\.5)?)(?![A-Za-z0-9.])')
        for match in numberPattern.finditer(cleanedName):
            episodeToken = match.group('episode')
            episode = self._parseEpisodeNumberToken(episodeToken)
            prefix = cleanedName[:match.start('episode')]
            suffix = cleanedName[match.end('episode'):]

            self._addNumericEpisodeFilenameCandidate(
                candidates, prefix, suffix, episode, None, episodeToken, "numeric")

            rangeMatch = re.match(r'(?P<separator>\s*(?:-|\+)\s*E?)(?P<episodeEnd>\d{1,3}(?:\.5)?)(?![A-Za-z0-9.])(?P<suffix>.*)$', suffix, re.I)
            if rangeMatch:
                episodeEnd = self._parseEpisodeNumberToken(rangeMatch.group('episodeEnd'))
                if episodeEnd > episode:
                    self._addNumericEpisodeFilenameCandidate(
                        candidates, prefix, rangeMatch.group('suffix'), episode, episodeEnd, episodeToken, "numericRange")

    def _addNumericEpisodeFilenameCandidate(self, candidates, prefix, suffix, episode, episodeEnd, episodeToken, candidateType):
        if not prefix and suffix:
            baseScore = 65
        else:
            suffixKey = self._normaliseEpisodeSuffixKey(suffix)
            baseScore = 70 if not suffixKey else 45

        self._addEpisodeFilenameCandidateFromParts(
            candidates,
            prefix,
            suffix,
            episode,
            episodeEnd,
            episodeToken,
            baseScore,
            candidateType,
            False,
            None,
        )

    def _addEpisodeFilenameCandidateFromParts(self, candidates, prefix, suffix, episode, episodeEnd, episodeToken, baseScore, candidateType, explicit, season):
        if episodeEnd is not None and episodeEnd < episode:
            return

        if not prefix and suffix:
            seriesKey = self._normaliseEpisodePrefix(suffix)
            suffixKey = ""
        else:
            seriesKey = self._normaliseEpisodePrefix(prefix)
            suffixKey = self._normaliseEpisodeSuffixKey(suffix)
        if not seriesKey:
            return

        candidate = {
            "seriesKey": seriesKey,
            "season": season,
            "episodeStart": episode,
            "episodeEnd": episodeEnd,
            "suffixKey": suffixKey,
            "baseScore": baseScore,
            "explicit": explicit,
            "episodeWidth": len(episodeToken.split('.')[0]),
            "candidateType": candidateType,
        }
        self._addEpisodeFilenameCandidate(candidates, candidate)

    def _addEpisodeFilenameCandidate(self, candidates, candidate):
        candidateKey = (
            candidate.get("seriesKey"),
            candidate.get("season"),
            candidate.get("episodeStart"),
            candidate.get("episodeEnd"),
            candidate.get("suffixKey"),
            candidate.get("candidateType"),
        )
        for existingCandidate in candidates:
            existingKey = (
                existingCandidate.get("seriesKey"),
                existingCandidate.get("season"),
                existingCandidate.get("episodeStart"),
                existingCandidate.get("episodeEnd"),
                existingCandidate.get("suffixKey"),
                existingCandidate.get("candidateType"),
            )
            if existingKey == candidateKey:
                if candidate.get("baseScore", 0) > existingCandidate.get("baseScore", 0):
                    existingCandidate.update(candidate)
                return
        candidates.append(candidate)

    def _chooseEpisodeFilenameCandidate(self, candidates, contextScores=None):
        explicitCandidates = [candidate for candidate in candidates if candidate.get("explicit")]
        if explicitCandidates:
            return self._getBestExplicitEpisodeFilenameCandidate(explicitCandidates)

        bestSingleCandidate = self._getBestSingleEpisodeFilenameCandidate(candidates)
        if not contextScores:
            return bestSingleCandidate

        bestContextCandidate = None
        bestContextScore = None
        for candidate in candidates:
            score = self._getEpisodeFilenameCandidateScore(candidate, contextScores)
            if bestContextScore is None or score > bestContextScore:
                bestContextCandidate = candidate
                bestContextScore = score

        if not bestContextCandidate:
            return bestSingleCandidate

        singleScore = self._getEpisodeFilenameCandidateScore(bestSingleCandidate, contextScores)
        if bestContextScore >= singleScore + 20:
            return bestContextCandidate
        return bestSingleCandidate

    def _getBestExplicitEpisodeFilenameCandidate(self, candidates):
        bestCandidate = None
        bestScore = None
        for candidate in candidates:
            score = self._getEpisodeFilenamePatternScore(candidate)
            score += self._getEpisodeFilenameExplicitScore(candidate)
            score += self._getEpisodeFilenameSuffixScore(candidate, explicit=True)
            if bestScore is None or score > bestScore:
                bestCandidate = candidate
                bestScore = score
        return bestCandidate

    def _getEpisodeFilenameExplicitScore(self, candidate):
        score = 0
        if candidate.get("season") is not None:
            score += 40
        if candidate.get("episodeEnd") is not None:
            score += 20
        if self._seriesKeyContainsEpisodeMarker(candidate.get("seriesKey")):
            score -= 50
        return score

    def _getBestSingleEpisodeFilenameCandidate(self, candidates):
        bestCandidate = None
        bestScore = None
        for candidate in candidates:
            score = self._getEpisodeFilenameCandidateScore(candidate, {})
            if bestScore is None or score > bestScore:
                bestCandidate = candidate
                bestScore = score
        return bestCandidate

    def _getEpisodeFilenameContextScores(self, contextFilenames):
        groups = {}
        for contextFilename in contextFilenames:
            cleanedName = self._normaliseEpisodeFilename(contextFilename)
            if not cleanedName:
                continue
            for candidate in self._getEpisodeFilenameCandidatesFromCleanedName(cleanedName):
                key = (candidate.get("seriesKey"), candidate.get("season"))
                group = groups.setdefault(key, {
                    "filenames": set(),
                    "episodeStarts": set(),
                    "episodes": set(),
                    "suffixes": set(),
                    "episodeWidths": set(),
                    "suffixHasEpisodeLikeNumber": False,
                })
                group["filenames"].add(cleanedName)
                episodeStart = candidate.get("episodeStart")
                episodeEnd = candidate.get("episodeEnd")
                if episodeEnd is None:
                    episodeEnd = episodeStart
                if episodeStart is None or episodeEnd is None:
                    continue
                group["episodeStarts"].add(episodeStart)
                for episodeNumber in self._getEpisodeNumbersInRange(episodeStart, episodeEnd):
                    group["episodes"].add(episodeNumber)
                suffixKey = candidate.get("suffixKey") or ""
                group["suffixes"].add(suffixKey)
                group["episodeWidths"].add(candidate.get("episodeWidth") or 0)
                if self._suffixContainsEpisodeLikeNumber(suffixKey):
                    group["suffixHasEpisodeLikeNumber"] = True

        contextScores = {}
        for key, group in groups.items():
            filenames = group.get("filenames", set())
            if len(filenames) < 2:
                continue

            episodeStarts = group.get("episodeStarts", set())
            episodes = group.get("episodes", set())
            suffixes = group.get("suffixes", set())
            score = 0

            if len(episodeStarts) > 1:
                score += 90
                if self._episodeNumbersLookConsecutive(episodeStarts):
                    score += 35
            else:
                score -= 80

            if len(episodes) > 1 and self._episodeNumbersLookConsecutive(episodes):
                score += 10

            if suffixes == set([""]):
                score += 35
            elif "" not in suffixes:
                score -= 30

            if group.get("suffixHasEpisodeLikeNumber"):
                score -= 50

            if max(group.get("episodeWidths", set([0]))) >= 2:
                score += 5

            seriesKey = key[0] or ""
            score += min(len(seriesKey), 35)
            contextScores[key] = score

        return contextScores

    def _episodeNumbersLookConsecutive(self, episodeNumbers):
        sortedEpisodes = sorted(episodeNumbers)
        previousEpisode = None
        for episodeNumber in sortedEpisodes:
            if previousEpisode is not None and 0 < episodeNumber - previousEpisode <= 1:
                return True
            previousEpisode = episodeNumber
        return False

    def _getEpisodeFilenameCandidateScore(self, candidate, contextScores):
        score = 0
        score += self._getEpisodeFilenamePatternScore(candidate)
        score += self._getEpisodeFilenameSeriesKeyScore(candidate)
        score += self._getEpisodeFilenameSuffixScore(candidate)
        score += self._getEpisodeFilenameContextScore(candidate, contextScores)
        return score

    def _getEpisodeFilenamePatternScore(self, candidate):
        score = candidate.get("baseScore", 0)
        if candidate.get("episodeWidth", 0) >= 3:
            score += 8
        elif candidate.get("episodeWidth", 0) >= 2:
            score += 5

        if candidate.get("candidateType") == "numericRange":
            if candidate.get("episodeEnd") is not None and not candidate.get("suffixKey"):
                score += 35
            else:
                score -= 15

        return score

    def _getEpisodeFilenameSeriesKeyScore(self, candidate):
        seriesKey = candidate.get("seriesKey") or ""
        return min(len(seriesKey), 35)

    def _getEpisodeFilenameContextScore(self, candidate, contextScores):
        if not contextScores:
            return 0
        return contextScores.get((candidate.get("seriesKey"), candidate.get("season")), 0)

    def _getEpisodeFilenameSuffixScore(self, candidate, explicit=False):
        suffixKey = candidate.get("suffixKey") or ""
        if not suffixKey:
            return 0 if explicit else 20

        if explicit:
            return -min(len(suffixKey), 30)

        seriesKey = candidate.get("seriesKey") or ""
        score = -10
        score -= min(len(suffixKey), 25)
        if self._suffixContainsEpisodeLikeNumber(suffixKey):
            score -= 50
        if len(suffixKey) > len(seriesKey):
            score -= 20
        return score

    def _suffixContainsEpisodeLikeNumber(self, suffixKey):
        if not suffixKey:
            return False
        return bool(re.search(r'(?i)(?:^|[\s._-])(?:e|ep|episode)?[\s._-]*\d{1,3}(?:\.5)?(?:$|[\s._-])', suffixKey))

    def _seriesKeyContainsEpisodeMarker(self, seriesKey):
        if not seriesKey:
            return False
        return bool(re.search(r'(?i)(?:s\d{1,2}\s*e\d{1,3}(?:\.5)?|\d{1,2}x\d{1,3}(?:\.5)?)', seriesKey))

    def _normaliseEpisodeFilename(self, filename):
        filename = os.path.splitext(os.path.basename(filename))[0]
        filename = self._stripLeadingEpisodeBracketTags(filename)
        filename = self._stripEpisodeFilenameNumericReleaseMetadata(filename)
        filename = re.sub(r'(?<=\d)\.(?=\d)', '<episode-decimal-point>', filename)
        filename = filename.replace('_', ' ')
        filename = filename.replace('.', ' ')
        filename = filename.replace('<episode-decimal-point>', '.')
        filename = re.sub(r'\s+', ' ', filename)
        return filename.strip()

    def _normaliseEpisodeSuffixKey(self, suffix):
        suffix = self._stripEpisodeFilenameReleaseMetadata(suffix)
        return self._normaliseEpisodePrefix(suffix)

    def _stripEpisodeFilenameNumericReleaseMetadata(self, filename):
        filename = re.sub(r'(?i)\[[0-9a-f]{8}\]', ' ', filename)
        filename = re.sub(r'(?i)\b\d{3,4}x\d{3,4}\b', ' ', filename)
        filename = re.sub(r'(?i)\b[257]\.1\b', ' ', filename)
        filename = re.sub(r'(?i)\b(?:h\.?26[45]|x26[45])\b', ' ', filename)
        filename = re.sub(r'(?i)\b(?:480p|576p|720p|1080p|2160p|4320p)\b', ' ', filename)
        filename = re.sub(r'(?i)\b(?:8bit|10bit|hi10p)\b', ' ', filename)
        return filename

    def _stripEpisodeFilenameReleaseMetadata(self, filename):
        filename = re.sub(r'(?i)\[[0-9a-f]{8}\]', ' ', filename)
        filename = re.sub(r'(?i)\b\d{3,4}x\d{3,4}\b', ' ', filename)
        filename = re.sub(r'(?i)\b[257]\.1\b', ' ', filename)
        filename = re.sub(r'(?i)\b(?:h\.?26[45]|x26[45]|avc|hevc|xvid|divx)\b', ' ', filename)
        filename = re.sub(r'(?i)\b(?:480p|576p|720p|1080p|2160p|4320p)\b', ' ', filename)
        filename = re.sub(r'(?i)\b(?:8bit|10bit|hi10p)\b', ' ', filename)
        filename = re.sub(r'(?i)\b(?:aac|ac3|flac|mp3|opus|vorbis)\b', ' ', filename)
        filename = re.sub(r'(?i)\b(?:hdtv|web[-\s]?dl|webrip|bluray|blu[-\s]?ray|bdrip|bdremux|remux|dvd|dvdrip|b[dr])\b', ' ', filename)
        filename = re.sub(r'(?i)[\[\(](?:v|version[\s._-]*)[2-7][\]\)]', ' ', filename)
        filename = re.sub(r'(?i)(?:^|[\s._-])(?:v|version[\s._-]*)[2-7](?=$|[\s._-])', ' ', filename)
        return filename

    def _stripLeadingEpisodeBracketTags(self, filename):
        while filename.startswith('['):
            end = filename.find(']')
            if end == -1:
                break
            filename = filename[end + 1:].lstrip()
        return filename

    def _normaliseEpisodePrefix(self, prefix):
        prefix = re.sub(r'\s+', ' ', prefix)
        prefix = prefix.strip(' -._')
        return prefix.lower()

    def getEpisodeNumbersInRange(self, episodeStart, episodeEnd):
        return self._getEpisodeNumbersInRange(episodeStart, episodeEnd)

    def isWholeEpisodeNumber(self, episodeNumber):
        return self._isWholeEpisodeNumber(episodeNumber)

    def normaliseEpisodeNumber(self, episodeNumber):
        return self._normaliseEpisodeNumber(episodeNumber)

    def _getEpisodeNumbersInRange(self, episodeStart, episodeEnd):
        if episodeStart is None or episodeEnd is None:
            return []
        if episodeEnd < episodeStart:
            return []
        if self._isWholeEpisodeNumber(episodeStart) and self._isWholeEpisodeNumber(episodeEnd):
            return list(range(int(episodeStart), int(episodeEnd) + 1))

        episodeNumbers = []
        currentEpisode = episodeStart
        while currentEpisode <= episodeEnd:
            episodeNumbers.append(self._normaliseEpisodeNumber(currentEpisode))
            currentEpisode += 0.5
        return episodeNumbers

    def _isWholeEpisodeNumber(self, episodeNumber):
        return int(episodeNumber) == episodeNumber

    def _normaliseEpisodeNumber(self, episodeNumber):
        if self._isWholeEpisodeNumber(episodeNumber):
            return int(episodeNumber)
        return episodeNumber



class WatchedManager(object):
    """
    Coordinator for the watched-file features:
    - Auto-move queue: pending moves to the watched subfolder, with retry/robustness logic.
    - Manual mark watched / unwatched actions.
    - JSON watched index: single config-adjacent .syncplay-watched.json (optional, disabled by default).

    SyncplayClient calls into this class only at:
      - updatePlayerStatus  -> processQueue()
      - playlist EOF/change hooks -> markCurrentFileWatched() / markFileWatched()
      - stop()               -> flushQueueOnShutdown()
    """

    def __init__(self, client):
        self._client = client
        self._episodeFilenameParser = EpisodeFilenameParser()
        self._pendingMoves = []        # list of normalised source paths
        self._attempts = {}            # path -> attempt count
        self._lastAttemptTime = 0.0
        # JSON index cache: jsonPath -> {"data": {filename: {...}}, "mtime": float}
        self._jsonCache = {}
        self._shownPlaylistWarningNotificationKeys = set()

    def _shouldUseWatchedHistoryInfo(self):
        return constants.WATCHED_HISTORY_ENABLED

    def _shouldUseWatchedSubfolderInfo(self):
        return constants.WATCHED_AUTOMOVE and len(constants.WATCHED_SUBFOLDER) > 0

    def _shouldUseWatchedFileInfo(self):
        return self._shouldUseWatchedHistoryInfo() or self._shouldUseWatchedSubfolderInfo()

    # ------------------------------------------------------------------
    # Public API called by SyncplayClient / GUI
    # ------------------------------------------------------------------

    def queueAutoMove(self, filePath):
        """Queue a file for auto-move to the watched subfolder."""
        if not filePath:
            return
        try:
            if utils.isURL(filePath):
                return
        except Exception:
            return

        try:
            pendingPath = os.path.normpath(os.path.abspath(filePath))
        except Exception:
            pendingPath = filePath

        try:
            pendingKey = os.path.normcase(pendingPath)
        except Exception:
            pendingKey = pendingPath

        existingKeys = []
        for existingPath in self._pendingMoves:
            try:
                existingKeys.append(os.path.normcase(os.path.normpath(os.path.abspath(existingPath))))
            except Exception:
                existingKeys.append(existingPath)

        if pendingKey not in existingKeys:
            self._pendingMoves.append(pendingPath)
            self._client.ui.showDebugMessage("Marked for watched move: {}".format(pendingPath))

    def markWatched(self, filePath):
        """Record a watched event immediately; queue a move only if auto-move is enabled."""
        if not filePath:
            return
        try:
            if utils.isURL(filePath):
                return
        except Exception:
            return
        correctedPath = utils.getCorrectedPathForFile(filePath)
        filename = os.path.basename(correctedPath)
        if constants.WATCHED_HISTORY_ENABLED:
            try:
                self._recordHistory("watched", filename)
            except Exception as e:
                self._client.ui.showDebugMessage(getMessage("watched-record-history-error").format(filename, e))
        if constants.WATCHED_AUTOMOVE:
            self.queueAutoMove(correctedPath)

    def markFileWatched(self, filePath):
        try:
            self.markWatched(filePath)
        except Exception as e:
            self._client.ui.showDebugMessage("Could not mark watched file: {}".format(e))

    def markCurrentFileWatched(self):
        try:
            currentFile = self._client.userlist.currentUser.file if self._client.userlist and self._client.userlist.currentUser else None
            currentFilePath = currentFile.get("path") if currentFile else None
            self.markWatched(currentFilePath)
        except Exception as e:
            self._client.ui.showDebugMessage("Could not mark watched file: {}".format(e))

    def processQueue(self):
        """Called periodically from updatePlayerStatus."""
        if not self._pendingMoves:
            return
        now = time.time()
        if (now - self._lastAttemptTime) < constants.WATCHED_CHECKQUEUE_INTERVAL:
            return
        self._lastAttemptTime = now
        self._tryMovePending()

    def flushQueueOnShutdown(self):
        """Called from stop(). Tries multiple times to handle file-in-use locks."""
        if not self._pendingMoves:
            return
        for _ in range(constants.WATCHED_PLAYERWAIT_MAXRETRIES):
            self._tryMovePending()
            if not self._pendingMoves:
                break
            time.sleep(constants.WATCHED_PLAYERWAIT_INTERVAL)

    def userMarkWatched(self, fileSourcePath):
        """Manual 'Mark as watched' context-menu action."""
        self._userInitiatedMoveToWatched(fileSourcePath)

    def userMarkUnwatched(self, fileSourcePath):
        """Manual 'Mark as unwatched' context-menu action."""
        self._userInitiatedMoveToParent(fileSourcePath)

    # ------------------------------------------------------------------
    # Auto-move queue processing
    # ------------------------------------------------------------------

    def _tryMovePending(self):
        if not constants.WATCHED_AUTOMOVE:
            if self._pendingMoves:
                self._client.ui.showDebugMessage(
                    "Auto-move to watched subfolder disabled; clearing {} pending move(s).".format(
                        len(self._pendingMoves)))
            self._pendingMoves = []
            self._attempts = {}
            return

        for srcPath in list(self._pendingMoves):
            try:
                if not os.path.exists(srcPath):
                    self._drop(srcPath, "Skipping watched move for '{}' because file no longer exists.".format(srcPath))
                    continue

                if not self._canMoveToWatchedSubfolder(srcPath):
                    self._drop(srcPath, "Skipping watched move for '{}' because it can no longer be auto-moved.".format(srcPath))
                    continue

                originalDir = os.path.dirname(srcPath)
                watchedDir = utils.getWatchedSubfolder(originalDir)
                if not watchedDir:
                    self._drop(srcPath, "Skipping watched move for '{}' because watched subfolder is not defined.".format(srcPath))
                    continue

                self._createWatchedSubdirIfNeeded(watchedDir)
                if not os.path.isdir(watchedDir):
                    self._drop(srcPath, "Skipping watched move for '{}' because watched subfolder '{}' is not a directory.".format(srcPath, watchedDir))
                    continue

                destPath = os.path.join(watchedDir, os.path.basename(srcPath))

                if os.path.exists(destPath):
                    self._client.ui.showErrorMessage(
                        getMessage("cannot-move-file-due-to-name-conflict-error").format(srcPath, constants.WATCHED_SUBFOLDER))
                    self._drop(srcPath, None)
                    continue

                try:
                    self._moveFile(srcPath, destPath)
                except FileExistsError:
                    self._client.ui.showErrorMessage(
                        getMessage("cannot-move-file-due-to-name-conflict-error").format(srcPath, constants.WATCHED_SUBFOLDER))
                    self._drop(srcPath, None)
                    continue

                # Successful move — dequeue unconditionally before notification
                self._drop(srcPath, None)
                self._client.fileSwitch.updateInfo()
                try:
                    self._client.ui.showMessage(
                        getMessage("moved-file-to-subfolder-notification").format(srcPath, constants.WATCHED_SUBFOLDER))
                except Exception as e:
                    self._client.ui.showDebugMessage("Moved watched file but could not notify: {}".format(e))

            except PermissionError:
                self._client.ui.showErrorMessage(
                    getMessage("watched-move-permission-error").format(srcPath))
                self._drop(srcPath, None)

            except Exception as e:
                msg = str(e).lower()
                retryable = ("in use" in msg) or ("being used" in msg) or ("sharing" in msg)
                if retryable:
                    self._noteAttempt(srcPath)
                    self._client.ui.showDebugMessage(
                        "Deferring watched move for '{}': {}".format(srcPath, e))
                else:
                    self._client.ui.showErrorMessage(
                        getMessage("watched-move-failed-error").format(srcPath, e))
                    self._drop(srcPath, None)

    def _noteAttempt(self, srcPath):
        self._attempts[srcPath] = self._attempts.get(srcPath, 0) + 1
        maxAttempts = getattr(constants, "WATCHED_MAX_MOVE_ATTEMPTS", None)
        if maxAttempts and self._attempts[srcPath] > maxAttempts:
            self._client.ui.showErrorMessage(
                getMessage("watched-move-too-many-retries-error").format(srcPath))
            self._drop(srcPath, None)

    def _drop(self, srcPath, debugMessage):
        if debugMessage:
            self._client.ui.showDebugMessage(debugMessage)
        try:
            self._pendingMoves.remove(srcPath)
        except ValueError:
            pass
        self._attempts.pop(srcPath, None)

    def _canMoveToWatchedSubfolder(self, filePath):
        if not filePath:
            return False
        if utils.isURL(filePath):
            return False
        if len(constants.WATCHED_SUBFOLDER) == 0:
            return False

        directory = utils.getCorrectedDirectoryForFile(filePath)
        if utils.isWatchedSubfolder(directory):
            return False

        watchedDirectory = utils.getWatchedSubfolder(directory)
        return bool((watchedDirectory and os.path.isdir(watchedDirectory)) or constants.WATCHED_AUTOCREATESUBFOLDERS)

    def _createWatchedSubdirIfNeeded(self, subfolderPath):
        if not subfolderPath:
            return
        if not constants.WATCHED_AUTOCREATESUBFOLDERS:
            return
        if not os.path.isdir(subfolderPath):
            os.makedirs(subfolderPath)

    def _moveFile(self, sourcePath, destinationPath):
        if os.path.exists(destinationPath):
            raise FileExistsError(destinationPath)
        shutil.move(sourcePath, destinationPath)

    # ------------------------------------------------------------------
    # Manual mark watched / unwatched
    # ------------------------------------------------------------------

    def _userInitiatedMoveToWatched(self, fileSourcePath):
        try:
            directory = os.path.dirname(fileSourcePath)
            filename = os.path.basename(fileSourcePath)

            if not self._shouldUseWatchedFileInfo():
                self._client.ui.showErrorMessage(
                    getMessage("watched-file-tracking-disabled-error"))
                return

            if not self._shouldUseWatchedSubfolderInfo():
                if self._shouldUseWatchedHistoryInfo():
                    self._recordHistory("watched", filename)
                self._client.fileSwitch.updateInfo()
                self._client.ui.showMessage(
                    getMessage("marked-file-as-watched-notification").format(filename))
                return

            watchedDirectory = utils.getWatchedSubfolder(directory)
            self._createWatchedSubdirIfNeeded(watchedDirectory)
            if not os.path.isdir(watchedDirectory):
                self._client.ui.showErrorMessage(
                    getMessage("watched-subfolder-unavailable-error").format(
                        fileSourcePath, constants.WATCHED_SUBFOLDER))
                return
            destPath = os.path.join(watchedDirectory, filename)
            watchedDirectoryName = os.path.basename(watchedDirectory) or constants.WATCHED_SUBFOLDER
            if os.path.exists(destPath):
                self._client.ui.showErrorMessage(
                    getMessage("cannot-move-file-due-to-name-conflict-error").format(fileSourcePath, watchedDirectoryName))
                return
            try:
                self._moveFile(fileSourcePath, destPath)
            except FileExistsError:
                self._client.ui.showErrorMessage(
                    getMessage("cannot-move-file-due-to-name-conflict-error").format(fileSourcePath, watchedDirectoryName))
                return
            if self._shouldUseWatchedHistoryInfo():
                self._recordHistory("watched", filename)
            self._client.fileSwitch.updateInfo()
            self._client.ui.showMessage(
                getMessage("moved-file-to-subfolder-notification").format(fileSourcePath, watchedDirectoryName))
        except Exception as e:
            self._client.ui.showErrorMessage(getMessage("watched-mark-watched-error").format(os.path.basename(fileSourcePath), e))
            self._client.ui.showDebugMessage(getMessage("watched-mark-watched-error").format(os.path.basename(fileSourcePath), e))

    def _userInitiatedMoveToParent(self, fileSourcePath):
        try:
            watchedDirectoryPath = os.path.dirname(fileSourcePath)
            filename = os.path.basename(fileSourcePath)

            # JSON-only mode: no watched subfolder configured, just remove from the index
            if len(constants.WATCHED_SUBFOLDER) == 0:
                if not constants.WATCHED_HISTORY_ENABLED:
                    self._client.ui.showErrorMessage(
                        getMessage("watched-file-tracking-disabled-error"))
                    return
                self._recordHistory("unwatched", filename)
                self._client.fileSwitch.updateInfo()
                self._client.ui.showMessage(
                    getMessage("marked-file-as-unwatched-notification").format(filename))
                return

            # Mixed mode: a file can be watched via JSON without physically being inside the watched subfolder.
            if constants.WATCHED_HISTORY_ENABLED and not utils.isWatchedSubfolder(watchedDirectoryPath):
                correctedPath = utils.getCorrectedPathForFile(fileSourcePath)
                if self.isWatchedFile(correctedPath):
                    self._recordHistory("unwatched", filename)
                    self._client.fileSwitch.updateInfo()
                    self._client.ui.showMessage(
                        getMessage("marked-file-as-unwatched-notification").format(filename))
                    return

            if not utils.isWatchedSubfolder(watchedDirectoryPath):
                self._client.ui.showErrorMessage(
                    getMessage("file-not-in-watched-subfolder-error").format(fileSourcePath))
                return
            parentDir = utils.getUnwatchedParentfolder(watchedDirectoryPath)
            if not parentDir:
                self._client.ui.showErrorMessage(
                    getMessage("watched-parent-folder-unavailable-error").format(fileSourcePath))
                return
            parentName = os.path.basename(parentDir)
            destPath = os.path.join(parentDir, filename)
            if os.path.exists(destPath):
                self._client.ui.showErrorMessage(
                    getMessage("cannot-move-file-due-to-parent-name-conflict-error").format(fileSourcePath, parentName))
                return
            try:
                self._moveFile(fileSourcePath, destPath)
            except FileExistsError:
                self._client.ui.showErrorMessage(
                    getMessage("cannot-move-file-due-to-parent-name-conflict-error").format(fileSourcePath, parentName))
                return
            try:
                self._recordHistory("unwatched", filename)
            except Exception as e:
                self._client.ui.showDebugMessage(getMessage("watched-record-history-error").format(filename, e))
            self._client.fileSwitch.updateInfo()
            self._client.ui.showMessage(
                getMessage("moved-file-from-watched-subfolder-notification").format(fileSourcePath, parentName))
        except Exception as e:
            self._client.ui.showErrorMessage(getMessage("watched-mark-unwatched-error").format(os.path.basename(fileSourcePath), e))
            self._client.ui.showDebugMessage(getMessage("watched-mark-unwatched-error").format(os.path.basename(fileSourcePath), e))

    def getSkippedEpisodeInfo(self, filename):
        """Return metadata about a likely skipped episode for the given playlist filename, or None."""
        if not self._shouldUseWatchedFileInfo():
            return None
        targetInfo = self._episodeFilenameParser.parse(filename)
        if not targetInfo:
            return None
        watchedEpisodeDetails = self._getWatchedEpisodeDetailsBySeries()
        watchedEpisodes = self._getWatchedEpisodesFromDetails(watchedEpisodeDetails)
        skipInfo = self._getSkippedEpisodeInfoFromParsed(targetInfo, watchedEpisodes)
        if skipInfo:
            self._addPreviousWatchedDetails(skipInfo, watchedEpisodeDetails)
        return skipInfo

    def maybeShowPlaylistWarningNotificationForFilename(self, playlistManager, filename):
        index = playlistManager.getPlaylistIndexFromPath(filename)
        if index is None:
            return
        self._maybeShowPlaylistWarningNotification(playlistManager, index)

    def _maybeShowPlaylistWarningNotification(self, playlistManager, index):
        warningText = self._getPlaylistWarningText(playlistManager._playlist, index)
        if not warningText:
            return
        try:
            filename = playlistManager._playlist[index]
        except (IndexError, TypeError):
            return
        warningKey = (filename, warningText)
        if warningKey in self._shownPlaylistWarningNotificationKeys:
            return
        self._shownPlaylistWarningNotificationKeys.add(warningKey)
        playlistManager._ui.showMessage(
            warningText,
            OSDType=constants.OSD_ALERT,
            mood=constants.MESSAGE_BADNEWS)

    def _getPlaylistWarningText(self, playlist, index):
        if playlist is None:
            return None
        try:
            filename = playlist[index]
        except (IndexError, TypeError):
            return None
        warningParts = []
        if constants.SHOW_PLAYLIST_ORDER_WARNINGS:
            playlistOrderWarnings = self.getPlaylistOrderWarnings(playlist)
        else:
            playlistOrderWarnings = {}
        orderWarning = playlistOrderWarnings.get(index)
        if constants.SHOW_PLAYLIST_ORDER_WARNINGS and orderWarning:
            warningParts.append(
                getMessage("playlist-out-of-order-warning-tooltip").format(
                    orderWarning["episode"], orderWarning["previousEpisode"], orderWarning["expectedEpisode"]))

        if constants.SHOW_PLAYLIST_SKIP_WARNINGS:
            playlistSkipWarnings = self.getPlaylistSkipWarnings(playlist)
        else:
            playlistSkipWarnings = {}
        skipWarning = playlistSkipWarnings.get(index)
        if constants.SHOW_PLAYLIST_SKIP_WARNINGS and skipWarning:
            warningParts.append(
                getMessage("playlist-skip-warning-tooltip").format(skipWarning["missingEpisode"]))
            previousWatchedTooltip = self._getWatchedTooltipForMetadata(skipWarning.get("previousWatchedMeta"))
            previousWatchedFilename = skipWarning.get("previousWatchedFilename")
            if previousWatchedTooltip and previousWatchedFilename:
                warningParts.append("'{}': {}".format(previousWatchedFilename, previousWatchedTooltip))

        return "\n".join(warningParts) if warningParts else None

    def _getWatchedTooltipForMetadata(self, meta):
        if not meta or not meta.get("lastWatchedAt"):
            return None
        try:
            dtUtc = datetime.datetime.strptime(meta["lastWatchedAt"], "%Y-%m-%dT%H:%M:%SZ").replace(
                tzinfo=datetime.timezone.utc)
            delta = datetime.datetime.now(datetime.timezone.utc) - dtUtc
            seconds = int(delta.total_seconds())
            if seconds < 3600:
                age = getMessage("watched-ago-minutes").format(max(1, seconds // 60))
            elif seconds < 86400:
                age = getMessage("watched-ago-hours").format(seconds // 3600)
            else:
                age = getMessage("watched-ago-days").format(delta.days)
            room = meta.get("lastRoom") or meta.get("lastWatchedRoom") or ""
            return getMessage("watched-last-watched-tooltip").format(
                age, room, dtUtc.astimezone().strftime(getMessage("watched-datetime-format")))
        except Exception:
            return None

    def getPlaylistSkipWarnings(self, playlist):
        """Return a dict mapping playlist indexes to likely skipped-episode warnings."""
        warnings = {}
        if not self._shouldUseWatchedFileInfo():
            return warnings

        watchedEpisodeDetails = self._getWatchedEpisodeDetailsBySeries()
        watchedEpisodes = self._getWatchedEpisodesFromDetails(watchedEpisodeDetails)
        playlistEpisodes = {}
        episodeContext = self._episodeFilenameParser.getContext(playlist)
        for index, filename in enumerate(playlist):
            targetInfo = self._episodeFilenameParser.parse(filename, context=episodeContext)
            if not targetInfo:
                continue

            seriesKey = (targetInfo["seriesKey"], targetInfo["season"])
            coveredEpisodes = set(watchedEpisodes.get(seriesKey, set()))
            coveredEpisodes.update(playlistEpisodes.get(seriesKey, set()))
            skipInfo = self._getSkippedEpisodeInfoFromParsed(
                targetInfo, watchedEpisodes, {seriesKey: coveredEpisodes})
            if skipInfo:
                self._addPreviousWatchedDetails(skipInfo, watchedEpisodeDetails)
                warnings[index] = skipInfo

            episodeStart = targetInfo.get("episodeStart")
            if episodeStart is not None:
                episodeEnd = targetInfo.get("episodeEnd")
                if episodeEnd is None:
                    episodeEnd = episodeStart
                episodes = playlistEpisodes.setdefault(seriesKey, set())
                for episodeNumber in self._getEpisodeNumbersInRange(episodeStart, episodeEnd):
                    episodes.add(episodeNumber)
        return warnings

    def _getSkippedEpisodeInfoFromParsed(self, targetInfo, watchedEpisodes, coveredEpisodes=None):
        seriesKey = (targetInfo["seriesKey"], targetInfo["season"])
        watchedSeriesEpisodes = watchedEpisodes.get(seriesKey, set())
        if coveredEpisodes is None:
            coveredEpisodes = watchedEpisodes
        coveredSeriesEpisodes = coveredEpisodes.get(seriesKey, set())

        targetStart = targetInfo["episodeStart"]
        if targetStart is None or not self._isWholeEpisodeNumber(targetStart) or targetStart < 3:
            return None
        if targetStart in coveredSeriesEpisodes:
            return None

        missingEpisode = self._normaliseEpisodeNumber(targetStart - 1)
        previousEpisode = self._normaliseEpisodeNumber(targetStart - 2)
        if missingEpisode in coveredSeriesEpisodes:
            return None
        if previousEpisode not in watchedSeriesEpisodes:
            return None

        return {
            "missingEpisode": missingEpisode,
            "previousEpisode": previousEpisode,
            "seriesKey": targetInfo["seriesKey"],
            "season": targetInfo["season"],
        }

    def getPlaylistOrderWarnings(self, playlist):
        """Return a dict mapping playlist indexes to first out-of-sequence warnings per show and season."""
        warnings = {}
        lastEpisodeByKey = {}
        flaggedKeys = set()
        episodeContext = self._episodeFilenameParser.getContext(playlist)

        for index, filename in enumerate(playlist):
            info = self._episodeFilenameParser.parse(filename, context=episodeContext)
            if not info:
                continue

            episodeStart = info.get("episodeStart")
            if episodeStart is None:
                continue

            key = (info["seriesKey"], info["season"])
            if key in flaggedKeys:
                lastEpisode = lastEpisodeByKey.get(key)
                episodeEnd = info.get("episodeEnd")
                if episodeEnd is None:
                    episodeEnd = episodeStart
                if lastEpisode is None or episodeEnd > lastEpisode:
                    lastEpisodeByKey[key] = episodeEnd
                continue

            lastEpisode = lastEpisodeByKey.get(key)
            if lastEpisode is None:
                episodeEnd = info.get("episodeEnd")
                if episodeEnd is None:
                    episodeEnd = episodeStart
                lastEpisodeByKey[key] = episodeEnd
                continue

            expectedEpisode = self._getExpectedEpisodeAfter(lastEpisode)
            if self._shouldWarnAboutEpisodeOrder(lastEpisode, episodeStart):
                warnings[index] = {
                    "expectedEpisode": expectedEpisode,
                    "previousEpisode": lastEpisode,
                    "episode": episodeStart,
                    "seriesKey": info["seriesKey"],
                    "season": info["season"],
                }
                flaggedKeys.add(key)

            episodeEnd = info.get("episodeEnd")
            if episodeEnd is None:
                episodeEnd = episodeStart
            if episodeEnd > lastEpisode:
                lastEpisodeByKey[key] = episodeEnd

        return warnings

    def _shouldWarnAboutEpisodeOrder(self, lastEpisode, episodeStart):
        # Warn for both backwards order, such as 03 -> 02, and forward gaps, such as 01 -> 03.
        if episodeStart <= lastEpisode:
            return True
        difference = episodeStart - lastEpisode
        if difference <= 1:
            return False
        return True

    def _getExpectedEpisodeAfter(self, episodeNumber):
        if self._isWholeEpisodeNumber(episodeNumber):
            return self._normaliseEpisodeNumber(episodeNumber + 1)
        return self._normaliseEpisodeNumber(int(episodeNumber) + 1)

    def _getEpisodeNumbersInRange(self, episodeStart, episodeEnd):
        return self._episodeFilenameParser.getEpisodeNumbersInRange(episodeStart, episodeEnd)

    def _isWholeEpisodeNumber(self, episodeNumber):
        return self._episodeFilenameParser.isWholeEpisodeNumber(episodeNumber)

    def _normaliseEpisodeNumber(self, episodeNumber):
        return self._episodeFilenameParser.normaliseEpisodeNumber(episodeNumber)

    def _getWatchedEpisodesBySeries(self):
        return self._getWatchedEpisodesFromDetails(self._getWatchedEpisodeDetailsBySeries())

    def _getWatchedEpisodesFromDetails(self, watchedEpisodeDetails):
        watchedEpisodes = {}
        for seriesKey, episodeDetails in watchedEpisodeDetails.items():
            watchedEpisodes[seriesKey] = set(episodeDetails.keys())
        return watchedEpisodes

    def _addPreviousWatchedDetails(self, skipInfo, watchedEpisodeDetails):
        seriesKey = (skipInfo["seriesKey"], skipInfo["season"])
        episodeDetails = watchedEpisodeDetails.get(seriesKey, {})
        previousEpisodeDetails = episodeDetails.get(skipInfo.get("previousEpisode"))
        if not previousEpisodeDetails:
            return
        skipInfo["previousWatchedFilename"] = previousEpisodeDetails.get("filename")
        skipInfo["previousWatchedMeta"] = previousEpisodeDetails.get("meta")

    def findSkippedFilePath(self, skipInfo):
        if not skipInfo:
            return None
        missingEpisode = skipInfo.get("missingEpisode")
        if missingEpisode is None:
            return None
        mediaFilesCache = getattr(self._client.fileSwitch, "mediaFilesCache", None)
        if not mediaFilesCache:
            return None

        matchingRangePath = None
        for directory, files in mediaFilesCache.items():
            episodeContext = self._episodeFilenameParser.getContext(files)
            for filename in files:
                info = self._episodeFilenameParser.parse(filename, context=episodeContext)
                if not info:
                    continue
                if info.get("seriesKey") != skipInfo.get("seriesKey"):
                    continue
                if info.get("season") != skipInfo.get("season"):
                    continue

                episodeStart = info.get("episodeStart")
                episodeEnd = info.get("episodeEnd")
                if episodeEnd is None:
                    episodeEnd = episodeStart
                if episodeStart is None or episodeEnd is None:
                    continue
                if episodeStart <= missingEpisode <= episodeEnd:
                    filepath = utils.getCorrectedPathForFile(os.path.join(directory, filename))
                    if not os.path.isfile(filepath):
                        continue
                    if episodeStart == missingEpisode:
                        return filepath
                    matchingRangePath = matchingRangePath or filepath

        return matchingRangePath

    def playlistContainsSkippedFile(self, playlist, skipInfo):
        if not skipInfo:
            return False
        missingEpisode = skipInfo.get("missingEpisode")
        if missingEpisode is None:
            return False

        episodeContext = self._episodeFilenameParser.getContext(playlist)
        for filename in playlist:
            info = self._episodeFilenameParser.parse(filename, context=episodeContext)
            if not info:
                continue
            if info.get("seriesKey") != skipInfo.get("seriesKey"):
                continue
            if info.get("season") != skipInfo.get("season"):
                continue

            episodeStart = info.get("episodeStart")
            episodeEnd = info.get("episodeEnd")
            if episodeEnd is None:
                episodeEnd = episodeStart
            if episodeStart is None or episodeEnd is None:
                continue
            if episodeStart <= missingEpisode <= episodeEnd:
                return True
        return False

    def _getWatchedEpisodeDetailsBySeries(self):
        watchedEpisodes = {}
        watchedItems = []

        if not self._shouldUseWatchedFileInfo():
            return watchedEpisodes

        if self._shouldUseWatchedHistoryInfo():
            jsonPath = self._getJsonPath()
            watchedData = self._loadJson(jsonPath)
            for filename, meta in watchedData.items():
                watchedItems.append((filename, meta))

        if self._shouldUseWatchedSubfolderInfo():
            mediaFilesCache = getattr(self._client.fileSwitch, "mediaFilesCache", None)
            if mediaFilesCache:
                for directory, files in mediaFilesCache.items():
                    if utils.isWatchedSubfolder(directory):
                        for filename in files:
                            watchedItems.append((filename, None))

        watchedFilenames = [filename for filename, meta in watchedItems]
        episodeContext = self._episodeFilenameParser.getContext(watchedFilenames)

        for filename, meta in watchedItems:
            info = self._episodeFilenameParser.parse(filename, context=episodeContext)
            if not info:
                continue
            seriesKey = (info["seriesKey"], info["season"])
            episodes = watchedEpisodes.setdefault(seriesKey, {})
            episodeEnd = info.get("episodeEnd")
            if episodeEnd is None:
                episodeEnd = info["episodeStart"]
            for episodeNumber in self._getEpisodeNumbersInRange(info["episodeStart"], episodeEnd):
                existingDetails = episodes.get(episodeNumber)
                if existingDetails and existingDetails.get("meta") and not meta:
                    continue
                episodes[episodeNumber] = {
                    "filename": filename,
                    "meta": meta,
                }

        return watchedEpisodes

    # ------------------------------------------------------------------
    # JSON watched index
    # ------------------------------------------------------------------

    def canMarkAsWatched(self, filePath):
        if not filePath:
            return False
        if utils.isURL(filePath):
            return False
        if not self._shouldUseWatchedFileInfo():
            return False
        if self.canMarkAsUnwatched(filePath):
            return False
        if self._shouldUseWatchedHistoryInfo():
            return True
        return self._canMoveToWatchedSubfolder(filePath)

    def canMarkAsUnwatched(self, filePath):
        if not filePath:
            return False
        if utils.isURL(filePath):
            return False
        return self.isWatchedFile(filePath) or self.isFileInWatchedSubfolder(filePath)

    def isFileInWatchedSubfolder(self, filePath):
        if not filePath:
            return False
        if utils.isURL(filePath):
            return False
        correctedPath = utils.getCorrectedPathForFile(filePath)
        if not correctedPath:
            return False
        directoryPath = os.path.dirname(correctedPath)
        return utils.isWatchedSubfolder(directoryPath) and os.path.exists(correctedPath)

    def isWatchedFile(self, filePath):
        if not filePath:
            return False
        if utils.isURL(filePath):
            return False

        correctedPath = utils.getCorrectedPathForFile(filePath)
        if not correctedPath:
            return False

        directoryPath = os.path.dirname(correctedPath)
        if self._shouldUseWatchedSubfolderInfo() and utils.isWatchedSubfolder(directoryPath) and os.path.exists(correctedPath):
            return True

        if not self._shouldUseWatchedHistoryInfo():
            return False

        filename = self._normaliseHistoryFilename(os.path.basename(correctedPath))
        if not filename:
            return False

        jsonPath = self._getJsonPath()
        watchedData = self._loadJson(jsonPath)
        return filename in watchedData

    def getWatchedMetadata(self, filePath):
        """Return the JSON metadata dict for filePath, or None if not in the index."""
        if not filePath or not constants.WATCHED_HISTORY_ENABLED or utils.isURL(filePath):
            return None
        correctedPath = utils.getCorrectedPathForFile(filePath)
        if not correctedPath:
            return None
        filename = self._normaliseHistoryFilename(os.path.basename(correctedPath))
        if not filename:
            return None
        jsonPath = self._getJsonPath()
        watchedData = self._loadJson(jsonPath)
        return watchedData.get(filename)

    def _normaliseHistoryFilename(self, filename):
        if not filename:
            return None
        filename = os.path.basename(filename)
        filename = os.path.normcase(filename)
        return filename

    def _getJsonPath(self):
        """Return the path to the single JSON index stored alongside the config file."""
        configDir = self._client._config["configDir"] or ""
        if not configDir:
            configPath = self._client._config["configPath"] or ""
            if configPath:
                configDir = os.path.dirname(os.path.abspath(configPath))
        if not configDir:
            if os.name == 'nt':
                configDir = os.getenv('APPDATA', '')
            else:
                configDir = os.getenv('XDG_CONFIG_HOME', '') or os.path.join(os.path.expanduser("~"), ".config")
        if not configDir:
            configDir = utils.findWorkingDir()
        return os.path.join(configDir, constants.WATCHED_HISTORY_FILENAME)

    def _loadJson(self, jsonPath):
        """Load (or reload) the single config-adjacent JSON watched index into cache."""
        try:
            mtime = os.path.getmtime(jsonPath)
        except OSError:
            mtime = None

        cached = self._jsonCache.get(jsonPath)
        if cached is not None and cached["mtime"] == mtime:
            return cached["data"]

        data = {}
        if mtime is not None:
            try:
                with open(jsonPath, "r", encoding="utf-8") as fh:
                    raw = fh.read()
                parsed = json.loads(raw)
                watched = parsed.get("watched", {})
                if isinstance(watched, dict):
                    for filename, metadata in watched.items():
                        normalisedFilename = self._normaliseHistoryFilename(filename)
                        if not normalisedFilename or not isinstance(metadata, dict):
                            continue
                        data[normalisedFilename] = metadata
            except Exception as e:
                self._client.ui.showDebugMessage(
                    getMessage("watched-json-read-error").format(jsonPath, e))
                data = {}
        self._jsonCache[jsonPath] = {"data": data, "mtime": mtime}
        return data

    def _writeJson(self, jsonPath, watchedData, expectedMtime=None):
        """Write the watched index to disk atomically (tmp + rename)."""
        tmpPath = jsonPath + ".tmp"
        try:
            directory = os.path.dirname(jsonPath)
            if directory and not os.path.isdir(directory):
                os.makedirs(directory, exist_ok=True)

            try:
                currentMtime = os.path.getmtime(jsonPath)
            except OSError:
                currentMtime = None
            if currentMtime != expectedMtime:
                return False

            payload = {"version": 1, "watched": watchedData}
            content = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True)
            with open(tmpPath, "w", encoding="utf-8") as fh:
                fh.write(content)
            os.replace(tmpPath, jsonPath)
            try:
                newMtime = os.path.getmtime(jsonPath)
            except OSError:
                newMtime = None
            self._jsonCache[jsonPath] = {"data": dict(watchedData), "mtime": newMtime}
            return True
        except Exception as e:
            self._client.ui.showErrorMessage(
                getMessage("watched-json-write-error").format(jsonPath, e))
            self._client.ui.showDebugMessage(
                getMessage("watched-json-write-error").format(jsonPath, e))
            try:
                os.remove(tmpPath)
            except OSError:
                pass
            return False

    def _recordHistory(self, action, filename):
        """Record or remove a watched entry in the single filename-keyed JSON index."""
        if not constants.WATCHED_HISTORY_ENABLED:
            return
        if not filename:
            return

        filename = self._normaliseHistoryFilename(filename)
        if not filename:
            return

        jsonPath = self._getJsonPath()
        retries = 3
        for _ in range(retries):
            watchedData = self._loadJson(jsonPath)
            cached = self._jsonCache.get(jsonPath, {})
            expectedMtime = cached.get("mtime")
            watchedData = dict(watchedData)

            if action == "unwatched":
                watchedData.pop(filename, None)
            else:
                now_str = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
                room = ""
                try:
                    room = self._client.getRoom() or ""
                except Exception:
                    pass
                watchedData[filename] = {
                    "lastWatchedAt": now_str,
                    "lastRoom": room,
                }

            if self._writeJson(jsonPath, watchedData, expectedMtime=expectedMtime):
                return

        self._client.ui.showDebugMessage(
            getMessage("watched-json-concurrent-update-error").format(jsonPath))
