#!/usr/bin/python

import internetarchive
from random import randint

mixtapes = []

# create a list of all of the mixtapes available
for i in internetarchive.search_items('collection:hiphopmixtapes'):
    mixtapes.append(i['identifier'])

# select a random mixtape
mixtape = mixtapes[randint(0,len(mixtapes))]

print mixtape


