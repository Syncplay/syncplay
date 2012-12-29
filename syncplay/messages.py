en = {
      "connecting" : "Attempting to connect to {}:{}"
      }

messages = {
           "en": en
           }

def getMessage(locale, type_):
    if(messages.has_key(locale)):
        if(messages[locale].has_key(type_)):
            return messages[locale][type_]
    if(messages["en"].has_key(type_)):
        return messages["en"][type_]
    else:
        raise KeyError()