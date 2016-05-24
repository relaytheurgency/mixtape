#!/usr/bin/python
'''Play a random mixtaple from archive.org hiphopmixtapes collection using python and mplayer'''

'''Requires internetarchive module'''
import internetarchive
from random import randint
import os

mixtapes = []

# create a list of all of the mixtapes available
for i in internetarchive.search_items('collection:hiphopmixtapes'):
    mixtapes.append(i['identifier'])

# select a random mixtape
mixtape = mixtapes[randint(0,len(mixtapes))]

print mixtape

command = "mplayer -msgcolor -msglevel all=0:demux=4:statusline=5 -playlist http://archive.org/download/" + mixtape + "/" + mixtape + "_vbr.m3u 2>/dev/null"

os.system(command)
