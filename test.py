
from internetarchive import search_items
from time import sleep

for i in search_items('collection:hiphopmixtapes').iter_as_items():
    # print all the things in metadata for the item
    print i.item_metadata['metadata'].keys()
    # it seems like artist is commonly attributed to a track
    # so see if the track has "artist"
    print i.item_metadata['files'][0].keys()
    # turns out some tracks don't have artists so we'll need to handle
    # exceptions. For instance, compilation albums or simply
    # tracks that didn't have that info encoded. We can either guess or skip
    print i.item_metadata['files'][0]['artist']
    
