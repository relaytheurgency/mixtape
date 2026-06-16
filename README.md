# mixtape

Archive.org has begun cataloging thousands of mixtapes from various collections on the web. This python script utilizes the Archive.org REST API to grab mixtapes to play natively. Users can choose to either hear a random mixtape or select a mixtape from an artist search.

## instructions

1. `git clone https://github.com/relaytheurgency/mixtape.git`
2. `cd mixtape && ./mixtape.py`

## optional: authentication

If you need to access private collections or circumvent rate limits, you can provide an Archive.org API key via environment variables:

```bash
export IA_ACCESS_KEY="your_access_key"
export IA_SECRET_KEY="your_secret_key"
```

## future work
* Command line options for things like continuous play of random tapes
* Create mixtape from individual songs pulled from other mixtapes by criteria (artist, year, genre)
* Better formatting
* Bundle for pip install
