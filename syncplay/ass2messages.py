# coding:utf8

# ass2messages.py,   dictionary to subtitle exporter to automate translation
# author sosie-js
# require my pythonfx mofied version adding fixes and del_line facility
#==========================================

# For relative imports to work
import os, sys; sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from pyonfx import *

# will include message_en.py a dictiatary of English messages for the syncplay gui
# https://raw.githubusercontent.com/Syncplay/syncplay/master/syncplay/messages_en.py
import messages_en


lang="fr"
dict_message_file="messages_"+lang
ass_message_file=dict_message_file+".ass"
dict_message_file=dict_message_file+".py"
print("Welcome on the ass file %s  to %s dictionary to exporter" % (dict_message_file,ass_message_file) )
print("-------------------------------------------------------------------------------------")
 
io = Ass(ass_message_file) 
meta, styles, lines = io.get_data()

#messages will hold the message dict
messages=messages_en.en
i=len(lines)
pos_time=0


dict={}
#the fist line of Untitled.ass, empty, will serve as template
for line in lines:
    dict[str(line.effect)]=str(line.raw_text)


script_dir=os.path.dirname(os.path.realpath(__file__))
path_input=os.path.join(script_dir,"messages_en.py")
input = open(path_input, "r", encoding="utf-8-sig")
template=input.read()
input.close()

note='# This file was mainly auto generated from ass2messages.py applied on '+ass_message_file+' to get these messages\n'
note+='# its format has been harmonized, values are always stored in doublequotes strings, \n'
note+='# if double quoted string in the value then they should be esacaped like this \\". There is\n'
note+='# thus no reason to have single quoted strings. Tabs \\t and newlines \\n need also to be escaped.\n' 
note+='# whith ass2messages.py which handles these issues, this is no more a nightmare to handle. \n'
note+='# I fixed partially messages_en.py serving as template. an entry should be added in messages.py:\n'
note+='# "'+lang+'": messages_'+lang+'.'+lang+',  . Produced by sosie - sos-productions.com\n\n'


template=template.replace('en = {',note+lang+' = {')

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

for key, value in messages.items():
    value=value.replace("&amp;","&")
    if(key == "LANGUAGE"):
        language=value
    source=('"%s": "%s"' % (key, escapeBackslashAndTabs(value)))
    target=('"%s": "%s"' % (key,dict[key]))
    print(key+ ': "'+value+'" => "'+dict[key]+'"')
    template=template.replace(source,target)
    source=('"%s": \'%s\'' % (key, escapeBackslashAndTabs(value)))
    target=('"%s": "%s"' % (key,escapeDoublequotes(dict[key])))
    template=template.replace(source,target)
template=template.replace('English dictionary',language+' dictionary')

path_output=os.path.join(script_dir,dict_message_file)
with open(path_output,"w") as f:
    f.write(template)
    
#print(template)
