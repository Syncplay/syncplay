# coding:utf8
from syncplay import constants

from . import messages_de
from . import messages_en
from . import messages_es
from . import messages_eo
from . import messages_fr
from . import messages_it
from . import messages_pt_PT
from . import messages_pt_BR
from . import messages_tr
from . import messages_ru
from . import messages_zh_CN
import re

# In alphabetical order
messages = {
    "de": messages_de.de,
    "en": messages_en.en,
    "es": messages_es.es,
    "eo": messages_eo.eo,
    "fr": messages_fr.fr,
    "it": messages_it.it,
    "pt_PT": messages_pt_PT.pt_PT,
    "pt_BR": messages_pt_BR.pt_BR,
    "tr": messages_tr.tr,
    "ru": messages_ru.ru,
    "zh_CN": messages_zh_CN.zh_CN,
    "CURRENT": None
}

no_osd_message_list = [
    "slowdown-notification",
    "revert-notification",
]

def getLanguages():
    langList = {}
    for lang in messages:
        if lang != "CURRENT":
            langList[lang] = getMessage("LANGUAGE", lang)
    return langList

def getLanguageTags():
    langList = {}
    for lang in messages:
        if lang != "CURRENT":
            langList[lang] = getMessage("LANGUAGE-TAG", lang)
    return langList

def isNoOSDMessage(message):
    for no_osd_message in no_osd_message_list:
        regex = "^" + getMessage(no_osd_message).replace("{}", ".+") + "$"
        regex_test = bool(re.match(regex, message))
        if regex_test:
            return True
    return False

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

def listMessages(languages):
    languageNames = []
    for language in languages:
        languageNames.append(messages[language]["LANGUAGE"])
    comparison = "Listing Syncplay messages in the following languages: {}.\n".format(", ".join(languageNames))
    for message in messages["en"]:
        comparison = comparison + "[{}]\n".format(message)
        for language in languages:
            languageName = messages[language]["LANGUAGE"]
            messageText = messages[language][message] if message in messages[language] else "<UNTRANSLATED>"
            comparison = comparison + "{}: {}\n".format(languageName, messageText)
        comparison = comparison + "\n"
    return comparison

# print(listMessages(["en","fi"]))

def getInitialLanguage():
    try:
        import sys
        frozen = getattr(sys, 'frozen', '')
        if frozen and frozen in 'macosx_app':
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

def populateLanguageArgument():
    languageTags = "/".join(getLanguageTags())
    langList = {}
    for lang in messages:
        if lang != "CURRENT":
            messages[lang]["language-argument"] = messages[lang]["language-argument"].format(languageTags)
    return langList

populateLanguageArgument()