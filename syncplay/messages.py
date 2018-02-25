# coding:utf8
from syncplay import constants

import messages_en
import messages_ru
import messages_de
import messages_it

messages = {
           "en": messages_en.en,
           "ru": messages_ru.ru,
           "de": messages_de.de,
           "it": messages_it.it,
           "CURRENT": None
           }

def getLanguages():
    langList = {}
    for lang in messages:
        if lang != "CURRENT":
            langList[lang] = getMessage("LANGUAGE", lang)
    return langList

def setLanguage(lang):
    messages["CURRENT"] = lang

def getMissingStrings():
    missingStrings = ""
    for lang in messages:
        if lang != "en" and lang != "CURRENT":
            for message in messages["en"]:
                if not messages[lang].has_key(message):
                    missingStrings = missingStrings + "({}) Missing: {}\n".format(lang, message)
            for message in messages[lang]:
                if not messages["en"].has_key(message):
                    missingStrings = missingStrings + "({}) Unused: {}\n".format(lang, message)

    return missingStrings

def getInitialLanguage():
    import locale
    try:
        initialLanguage = locale.getdefaultlocale()[0].split("_")[0]
        if not messages.has_key(initialLanguage):
            initialLanguage = constants.FALLBACK_INITIAL_LANGUAGE
    except:
        initialLanguage = constants.FALLBACK_INITIAL_LANGUAGE
    return initialLanguage

def isValidLanguage(language):
    return messages.has_key(language)

def getMessage(type_, locale=None):
    if constants.SHOW_TOOLTIPS == False:
        if "-tooltip" in type_:
            return ""

    if not isValidLanguage(messages["CURRENT"]):
        setLanguage(getInitialLanguage())

    lang = messages["CURRENT"]
    if locale and messages.has_key(locale):
        if messages[locale].has_key(type_):
            return unicode(messages[locale][type_])
    if lang and messages.has_key(lang):
        if messages[lang].has_key(type_):
            return unicode(messages[lang][type_])
    if messages["en"].has_key(type_):
        return unicode(messages["en"][type_])
    else:
        print u"WARNING: Cannot find message '{}'!".format(type_)
        return "!{}".format(type_) # TODO: Remove
        #raise KeyError(type_)
