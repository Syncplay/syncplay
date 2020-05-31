# coding:utf8
from syncplay import constants

from . import messages_en
from . import messages_ru
from . import messages_de
from . import messages_it
from . import messages_es
from . import messages_pt_BR
from . import messages_pt_PT

messages = {
    "en": messages_en.en,
    "ru": messages_ru.ru,
    "de": messages_de.de,
    "it": messages_it.it,
    "es": messages_es.es,
    "pt_BR": messages_pt_BR.pt_BR,
    "pt_PT": messages_pt_PT.pt_PT,
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
                if message not in messages[lang]:
                    missingStrings = missingStrings + "({}) Missing: {}\n".format(lang, message)
            for message in messages[lang]:
                if message not in messages["en"]:
                    missingStrings = missingStrings + "({}) Unused: {}\n".format(lang, message)

    return missingStrings


def getInitialLanguage():
    try:
        import sys
        frozen = getattr(sys, 'frozen', '')
        if frozen in 'macosx_app':
            from PySide2.QtCore import QLocale
            initialLanguage = QLocale.system().uiLanguages()[0].split('-')[0]
        else:
            import locale
            initialLanguage = locale.getdefaultlocale()[0].split("_")[0]
        if initialLanguage not in messages:
            initialLanguage = constants.FALLBACK_INITIAL_LANGUAGE
    except:
        initialLanguage = constants.FALLBACK_INITIAL_LANGUAGE
    return initialLanguage


def isValidLanguage(language):
    return language in messages


def getMessage(type_, locale=None):
    if constants.SHOW_TOOLTIPS == False:
        if "-tooltip" in type_:
            return ""

    if not isValidLanguage(messages["CURRENT"]):
        setLanguage(getInitialLanguage())

    lang = messages["CURRENT"]
    if locale and locale in messages:
        if type_ in messages[locale]:
            return str(messages[locale][type_])
    if lang and lang in messages:
        if type_ in messages[lang]:
            return str(messages[lang][type_])
    if type_ in messages["en"]:
        return str(messages["en"][type_])
    else:
        print("WARNING: Cannot find message '{}'!".format(type_))
        #return "!{}".format(type_)  # TODO: Remove
        raise KeyError(type_)
