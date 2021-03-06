#!/usr/bin/env python
__author__ = "Brandon Jones"
__copyright__ = "Copyright 2016, Brandon Jones"
__license__ = "MIT License"
__version__ = "1.0.0"
__email__ = "jones.brandon.lee@gmail.com"

'''Play a random mixtape from archive.org hiphopmixtapes collection using python and mplayer'''
import internetarchive
from random import randint
import os

# Handle input/raw_input switch so I don't have to worry about versions
# for simple inputs
real_raw_input = vars(__builtins__).get('raw_input',input)

def random_or_artist():
    '''Have the user choose whether to search for a specific artist or play a random tape'''
    
    choice = real_raw_input("\
Would you like to: \n\
a) Play a random mixtape \n\
b) Choose an artist? \n\
q) quit (a/b/q): ")
    
    if choice == "a":
        play_tape(random_mixtape())
    elif choice == "b":
        play_tape(artist_mixtape(search_artist(get_artist())))
    elif choice == "q":
        exit()
    else:
        print("Please make a valid choice!")
        random_or_artist()

def get_artist():
    '''Get artist from user'''
    
    artist_name = real_raw_input("Which artist would you like to listen to?: ")
    return artist_name

def search_artist(artist_name):
    '''Search archive.org for tapes from an artist and return those tapes'''    

    artist_tapes = internetarchive.search_items('collection:hiphopmixtapes AND title:' + artist_name)
    return artist_tapes

def random_mixtape():
    '''Return a random mixtape item'''
    
    mixtapes=[]

    for i in internetarchive.search_items('collection:hiphopmixtapes'):
        mixtapes.append(i['identifier'])

    # select a random mixtape
    mixtape = mixtapes[randint(0,len(mixtapes) - 1)]
    return mixtape

def artist_mixtape(artist_search):
    '''Returns an artist specific mixtape the user chooses from'''

    mixtapes = []
    for i in artist_search:
        mixtapes.append(i['identifier'])
    
    if len(mixtapes) == 0:
        print("Your search yielded no results! Try again!")
        return artist_mixtape(search_artist(get_artist()))
    else:
        print("Choose which mixtape you would like to play by entering the corresponding number:\n")
        for i in range(len(mixtapes)):
            print(str(i) + ". " + str(mixtapes[i]))
        
        choice = real_raw_input("Choice (b to search again): ")
        if choice == "b":
            return artist_mixtape(search_artist(get_artist()))
        elif choice.isdigit() == False or (int(choice) < 0 or int(choice) > (len(mixtapes) - 1)):
            print("Please enter a valid digit.")
            return artist_mixtape(artist_search)
        else:
            mixtape = mixtapes[int(choice)]
            return mixtape

def play_tape(mixtape):
    '''Calls mplayer to play a mixtape'''

    print("Now playing " + mixtape)
    command = "mplayer -msgcolor -msglevel all=0:demux=5:statusline=5 -playlist http://archive.org/download/" + mixtape + "/" + mixtape + "_vbr.m3u 2>/dev/null"
    os.system(command)
    print("\n")

    random_or_artist()

random_or_artist()
