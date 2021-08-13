# coding:utf8
#
# ass2messages.py,   ass subtitle to dictionary converter
# version 2.0
# author sosie-js - sos-productions.com
#==========================================

# For relative imports to work, to use my  pythonfx mofied version adding fixes and del_line facility
import os, sys; sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from pyonfx import *

#message_en.py  hold the original English messages we translte from  for the syncplay gui
# https://raw.githubusercontent.com/Syncplay/syncplay/master/syncplay/messages_en.py
# this will serves aslo as a template to generate dict_message_file
import messages_en
messages=messages_en.en

#here is the only param for this script,  the target language, it requires the ass file ass_message_file, holding the translated messages
# we use messages2ass.py on messages_en.py to generate messages_en.ass and then we fastrad it with google translate/deepl ... 
#to have it in the targetted language
lang="fr"

#----------------------------------------------------------
dict_message_file="messages_"+lang
ass_message_file=dict_message_file+".ass"
dict_message_file=dict_message_file+".py"
print("Welcome on the ass file %s  to %s dictionary to exporter" % (dict_message_file,ass_message_file) )
print("-------------------------------------------------------------------------------------")

#Generate translations dictionary from the translated messages provided by ass_message_file 

io = Ass(ass_message_file) 
meta, styles, lines = io.get_data()

dict={}
for line in lines:
    dict[str(line.effect)]=str(line.raw_text)

script_dir=os.path.dirname(os.path.realpath(__file__))
path_input=os.path.join(script_dir,"messages_en.py")
input = open(path_input, "r", encoding="utf-8-sig")
template=input.read()
input.close()

#Normalize space (and quotes!), launch the cleaner machine

template=template.replace('":  "','": "')
template=template.replace('":  \'','": \'')

def escapeBackslashAndTabs(s):
    s = s.replace("\t", "\\t")
    s = s.replace("\n", "\\n")
    return s

def escapeDoublequotes(s):
    s = s.replace('"', '\\"')
    return s     

def decodeHTMLEntities(s):
    s = s.replace("&gt;", ">")
    s = s.replace("&amp;","&")
    return s      
    
#Now fill the template

note='# This file was mainly auto generated from ass2messages.py applied on '+ass_message_file+' to get these messages\n'
note+='# its format has been harmonized, values are always stored in doublequotes strings, \n'
note+='# if double quoted string in the value then they should be esacaped like this \\". There is\n'
note+='# thus no reason to have single quoted strings. Tabs \\t and newlines \\n need also to be escaped.\n' 
note+='# whith ass2messages.py which handles these issues, this is no more a nightmare to handle. \n'
note+='# I fixed partially messages_en.py serving as template. an entry should be added in messages.py:\n'
note+='# "'+lang+'": messages_'+lang+'.'+lang+',  . Produced by sosie - sos-productions.com\n\n'

template=template.replace('en = {',note+lang+' = {')

for key, value in messages.items():
    value=decodeHTMLEntities(value)
    if(key == "LANGUAGE"):
        language=value
    source=('"%s": "%s"' % (key, escapeBackslashAndTabs(value)))
    target=('"%s": "%s"' % (key,dict[key]))
    print(key+ ': "'+value+'" => "'+dict[key]+'"')
    template=template.replace(source,target)
    source=('"%s": \'%s\'' % (key, escapeBackslashAndTabs(value)))
    target=('"%s": "%s"' % (key,escapeDoublequotes(dict[key])))
    template=template.replace(source,target)
    
#this line does nothing, I don't know why :(
template=template.replace('English dictionary',language+' dictionary')

# Save it as .ass file
path_output=os.path.join(script_dir,dict_message_file)
with open(path_output,"w") as f:
    f.write(template)
    
#print(template)
