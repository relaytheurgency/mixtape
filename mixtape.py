#!/usr/bin/python
'''Play a random mixtape from archive.org hiphopmixtapes collection using python and mplayer'''

'''Requires internetarchive module'''
import internetarchive
from random import randint
import os

# Handle input/raw_input switch so I don't have to worry about versions
# for simple inputs
real_raw_input = vars(__builtins__).get('raw_input',input)

def random_or_artist():
    
    choice = real_raw_input("Would you like to a) Play a random mixtape or b) Choose an artist? (a/b): ")
    
    if choice == "a":
        play_tape(random_mixtape())
    elif choice == "b":
        play_tape(artist_mixtape(search_artist(get_artist())))
    else:
        print("You didn't choose either, defaulting to random mixtape!")
        play_tape(random_mixtape())

def get_artist():
    '''Get artist from user'''
    
    artist_name = real_raw_input("Which artist would you like to listen to?: ")
    return artist_name

def search_artist(artist_name):
    '''Search archive.org for tapes from an artist'''    

    artist_tapes = internetarchive.search_items('collection:hiphopmixtapes AND title:' + artist_name)
    
    return artist_tapes

def random_mixtape():

    mixtapes=[]

    for i in internetarchive.search_items('collection:hiphopmixtapes'):
        mixtapes.append(i['identifier'])

    # select a random mixtape
    mixtape = mixtapes[randint(0,len(mixtapes))]

    return mixtape

def artist_mixtape(artist_search):
    
    mixtapes = []
    for i in artist_search:
        mixtapes.append(i['identifier'])

    mixtape = mixtapes[randint(0,len(mixtapes))]

    return mixtape

def play_tape(mixtape):

    command = "mplayer -msgcolor -msglevel all=0:demux=5:statusline=5 -playlist http://archive.org/download/" + mixtape + "/" + mixtape + "_vbr.m3u 2>/dev/null"
    os.system(command)

random_or_artist()
