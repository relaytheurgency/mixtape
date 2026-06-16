#!/usr/bin/env python3
__author__ = "Brandon Jones"
__copyright__ = "Copyright 2016, Brandon Jones"
__license__ = "MIT License"
__version__ = "1.0.0"
__email__ = "jones.brandon.lee@gmail.com"

'''Play a random mixtape from archive.org hiphopmixtapes collection using python and mplayer'''

import json
import urllib.request
import urllib.parse
from random import randint
import os
import sys
import tempfile
import platform
import subprocess

def get_api_headers():
    headers = {}
    access_key = os.environ.get("IA_ACCESS_KEY")
    secret_key = os.environ.get("IA_SECRET_KEY")
    if access_key and secret_key:
        headers["Authorization"] = f"LOW {access_key}:{secret_key}"
    return headers

def perform_search(query):
    params = {
        'q': query,
        'fl[]': 'identifier',
        'rows': 10000,
        'output': 'json'
    }
    url = "https://archive.org/advancedsearch.php?" + urllib.parse.urlencode(params, doseq=True)
    req = urllib.request.Request(url, headers=get_api_headers())
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data.get('response', {}).get('docs', [])
    except Exception as e:
        print(f"Error communicating with archive.org: {e}")
        return []

def random_or_artist():
    '''Have the user choose whether to search for a specific artist or play a random tape'''
    while True:
        try:
            choice = input("\
Would you like to: \n\
a) Play a random mixtape \n\
b) Choose an artist? \n\
q) quit (a/b/q): ")

            if choice == "a":
                tape = random_mixtape()
                if tape:
                    play_tape(tape)
            elif choice == "b":
                artist_name = get_artist()
                tapes = search_artist(artist_name)
                tape = artist_mixtape(tapes, artist_name)
                if tape:
                    play_tape(tape)
            elif choice == "q":
                sys.exit(0)
            else:
                print("Please make a valid choice!")
        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")
            sys.exit(0)

def get_artist():
    '''Get artist from user'''
    return input("Which artist would you like to listen to?: ")

def search_artist(artist_name):
    '''Search archive.org for tapes from an artist and return those tapes'''
    query = 'collection:(hiphopmixtapes) AND title:(' + artist_name + ')'
    return perform_search(query)

def random_mixtape():
    '''Return a random mixtape item'''
    docs = perform_search('collection:(hiphopmixtapes)')
    if not docs:
        print("No mixtapes found.")
        return None

    mixtape = docs[randint(0, len(docs) - 1)]['identifier']
    return mixtape

def artist_mixtape(artist_search, artist_name):
    '''Returns an artist specific mixtape the user chooses from'''
    mixtapes = [i['identifier'] for i in artist_search if 'identifier' in i]

    if len(mixtapes) == 0:
        print("Your search yielded no results! Try again!")
        return artist_mixtape(search_artist(get_artist()), artist_name)
    else:
        print("\nChoose which mixtape you would like to play by entering the corresponding number:\n")
        for i in range(len(mixtapes)):
            print(str(i) + ". " + str(mixtapes[i]))

        choice = input("\nChoice (b to search again): ")
        if choice == "b":
            return artist_mixtape(search_artist(get_artist()), artist_name)
        elif not choice.isdigit() or int(choice) < 0 or int(choice) > (len(mixtapes) - 1):
            print("Please enter a valid digit.")
            return artist_mixtape(artist_search, artist_name)
        else:
            return mixtapes[int(choice)]

def get_play_command(filepath):
    system = platform.system()
    if system == "Darwin":
        return ["afplay", filepath]
    elif system == "Linux":
        return ["paplay", filepath]
    elif system == "Windows":
        return ["cmd.exe", "/c", "start", "/wait", filepath]
    return []

def fetch_metadata(identifier):
    url = f"https://archive.org/metadata/{identifier}"
    try:
        req = urllib.request.Request(url, headers=get_api_headers())
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"Error fetching metadata: {e}")
        return {}

def play_tape(mixtape):
    '''Parses the M3U playlist, downloads tracks, and plays them natively with metadata'''
    try:
        print(f"\nFetching metadata for {mixtape}...")
        metadata = fetch_metadata(mixtape)

        meta_info = metadata.get('metadata', {})
        title = meta_info.get('title') or mixtape

        creator = meta_info.get('creator') or meta_info.get('artist')
        year = meta_info.get('year') or meta_info.get('date')

        if not year:
            publicdate = meta_info.get('publicdate', '')
            if publicdate and len(publicdate) >= 4:
                year = publicdate[:4]

        if not creator:
            for f in metadata.get('files', []):
                if f.get('name', '').endswith('.mp3'):
                    creator = f.get('creator') or f.get('artist')
                    if creator:
                        break

        creator = creator or 'Unknown Artist'
        year = year or 'Unknown Year'

        print("\n" + "="*40)
        print(f"=== MIXTAPE: {title}")
        print(f"=== ARTIST:  {creator}")
        print(f"=== YEAR:    {year}")
        print("="*40 + "\n")

        # Build a file metadata lookup
        file_metadata = {}
        for f in metadata.get('files', []):
            if f.get('name', '').endswith('.mp3'):
                file_metadata[f['name']] = f
                # Also store url-encoded version just in case
                file_metadata[urllib.parse.quote(f['name'])] = f

        print(f"Fetching playlist for {mixtape}...")
        m3u_url = f"http://archive.org/download/{mixtape}/{mixtape}_vbr.m3u"

        try:
            req = urllib.request.Request(m3u_url, headers=get_api_headers())
            with urllib.request.urlopen(req) as response:
                m3u_content = response.read().decode('utf-8')
        except Exception as e:
            print(f"Error fetching playlist: {e}")
            return

        # Parse M3U
        tracks = [line.strip() for line in m3u_content.split('\n') if line.strip() and not line.startswith('#')]

        if not tracks:
            print("No tracks found in the playlist.")
            return

        print(f"Found {len(tracks)} tracks. Starting playback...")

        for idx, track_url in enumerate(tracks):
            track_filename = urllib.parse.unquote(track_url.split('/')[-1])
            print(f"\n[{idx+1}/{len(tracks)}] Downloading: {track_filename} ...")

            # Look up track metadata
            fm = file_metadata.get(track_url.split('/')[-1], {})
            if not fm:
                fm = file_metadata.get(track_filename, {})

            track_title = fm.get('title', track_filename)
            track_artist = fm.get('creator') or fm.get('artist') or creator
            track_album = fm.get('album', title)
            track_length = fm.get('length', 'Unknown length')

            temp_path = None
            try:
                # Download to a temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
                    temp_path = temp_audio.name

                    # Clean the URL to avoid "URL can't contain control characters" errors
                    parsed_url = urllib.parse.urlparse(track_url)
                    safe_path = urllib.parse.quote(urllib.parse.unquote(parsed_url.path))
                    clean_track_url = urllib.parse.urlunparse(
                        (parsed_url.scheme, parsed_url.netloc, safe_path, parsed_url.params, parsed_url.query, parsed_url.fragment)
                    )

                    track_req = urllib.request.Request(clean_track_url, headers=get_api_headers())
                    with urllib.request.urlopen(track_req) as track_resp:
                        temp_audio.write(track_resp.read())

                print(f"Playing: {track_title}")
                if track_artist and track_artist != 'Unknown Artist':
                    print(f"  Artist: {track_artist}")
                if track_album and track_album != mixtape:
                    print(f"  Album:  {track_album}")
                print(f"  Length: {track_length}")
                print("(Press Ctrl+C to skip track)")

                play_cmd = get_play_command(temp_path)

                if play_cmd:
                    try:
                        subprocess.run(play_cmd)
                    except KeyboardInterrupt:
                        print("\nSkipping track... (Press Ctrl+C again quickly to abandon mixtape)")
                        import time
                        time.sleep(1.5)
                    except FileNotFoundError:
                        print(f"\nCould not find native audio player for OS {platform.system()}. Skipping.")
                else:
                    print(f"Unsupported OS for native playback: {platform.system()}")

            except KeyboardInterrupt:
                raise # re-raise to be caught by the outer try block to abandon the mixtape
            except Exception as e:
                print(f"Error playing track: {e}")
            finally:
                # Clean up the temp file
                if temp_path and os.path.exists(temp_path):
                    os.remove(temp_path)

        print("\nMixtape finished.")
    except KeyboardInterrupt:
        print("\nAbandoning mixtape and returning to main menu...")
        return

if __name__ == "__main__":
    random_or_artist()
