#!/usr/bin/python
'''Play a random mixtaple from archive.org hiphopmixtapes collection using python and mplayer'''

'''Requires internetarchive module'''
import internetarchive
from random import randint
import os


def search_artist(artist_name):
    '''Search archive.org for tapes from an artist'''    
    artist_tapes = search_items('collection:hiphopmixtapes AND title:' + artist_name)
    
    for tape in artist_tapes:
        print tape['identifier']

    return artist_tapes


def random_mixtape():
    # create a list of all of the mixtapes available

    mixtapes=[]

    for i in internetarchive.search_items('collection:hiphopmixtapes'):
        mixtapes.append(i['identifier'])

    # select a random mixtape
    mixtape = mixtapes[randint(0,len(mixtapes))]

    return mixtape

def play_tape(mixtape):

    command = "mplayer -msgcolor -msglevel all=0:demux=5:statusline=5 -playlist http://archive.org/download/" + mixtape + "/" + mixtape + "_vbr.m3u 2>/dev/null"
    os.system(command)


play_tape(random_mixtape())
