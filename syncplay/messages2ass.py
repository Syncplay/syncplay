# coding:utf8

# messages2ass.py,   dictionary to subtitle exporter to automate translation
# version 2.0 
# author sosie-js
# require my pythonfx mofied version adding fixes and del_line facility
#==========================================

# For relative imports to work, ie use my local version of pythonfx
import os, sys; sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from pyonfx import *

#choose your wished language target, a matching dict_message_file must be provided
lang="en"

#------------------------------------------------------------
dict_message_file="message_"+lang #.py
ass_message_file=dict_message_file+".ass"
print("Welcome on the %s dictionary to ass file %s exporter" % (dict_message_file,ass_message_file) )
print("-------------------------------------------------------------------------------------")
 
io = Ass() #Will use aegisub template Untitled.ass as basis instead of "in.ass"
io.set_output(ass_message_file)
meta, styles, lines = io.get_data()

#include by string the <lang> messages file to convert to ass
# name=messages_<lang>.<lang>
#as lang is 'en', it will include message_en.py a dictionary of English messages for the syncplay gui
# https://raw.githubusercontent.com/Syncplay/syncplay/master/syncplay/messages_en.py
#equivalent to messages=messages_en.en
def my_import(name):
    components = name.split('.')
    mod = __import__(components[0])
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod
    
#messages will hold the ditionary of messages for the language lang
messages=my_import('messages_'+lang+'.'+lang)
i=len(lines)
pos_time=0

#the fist line of Untitled.ass, empty, will serve as template
line= lines[0].copy()
duration=2000

for key, value in messages.items():
    print("Exporting value of key %s as subtiyle line" % key)
    l= line.copy()
    i=i+1
    l.i=i
    l.start_time = pos_time
    l.end_time = pos_time+duration
    l.effect= key
    l.text =value
    io.write_line(l)
    pos_time=pos_time+duration

#Don't forget to remove the pollution lines of the template 
# in our case remove the empty single line of Untitled.ass.
io.del_line(1)   

io.save()
io.open_aegisub()