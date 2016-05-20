# mixtape

This is a really, really sloppy way to play random mixtapes on the command line from archive.org's hiphopmixtapes collection. Any improvements are more than welcome. The OS X version has been tested, I'm assuming the other version will work fine on any system that has GNU sort as `sort`.

## dependencies

[ia] (http://developers.archive.org/services/ia-v1/) (See below if you don't want to use ia)

[mplayer] (http://www.mplayerhq.hu/design7/news.html)

coreutils (this should be installed already on linux, but you'll need to `brew install coreutils` on OS X to get GNU sort)

## caveats

You're going to have to CTRL-C twice in succession to exit because I was too lazy to do this appropriately (just wanted some tunes)!
You'll want to register for an official account at archive.org and then run `ia configure` to get everything set up for this to work.

UNLESS!! If you don't want to register an account you can use the 'sloppiest' scripts which use a terrible, terrible curl to get a random mixtape to play.
