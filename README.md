# mixtape

Archive.org has begun cataloging thousands of mixtapes from various collections on the web. This python script utilizes Archive.org's `internetarchive` python module to grab random mixtapes to play through mplayer.

## dependencies

[ia] (http://developers.archive.org/services/ia-v1/)  
[mplayer] (http://www.mplayerhq.hu/design7/news.html)  
python
pip  

## instructions

1. Download mplayer for your distribution/OS
2. Register for an account at archive.org
3. `pip install internetarchive`
4. `ia configure`
5. `git clone https://github.com/relaytheurgency/mixtape.git`
6. `cd mixtape && ./mixtape.py`

## caveats

I have included a bash script for those that don't want to register at archive.org. The caveat here is that this script uses a pretty sloppy `curl` and is not guaranteed to work for any forseeable future. To use the bash script just clone the repo and execute as you would any other script. It only requires mplayer if you're on linux. If you are on OS X you will need to `brew install coreutils`
