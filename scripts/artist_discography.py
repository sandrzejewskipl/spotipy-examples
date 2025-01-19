# Shows the list of all songs sung by the artist or the band
import argparse
import logging

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

logger = logging.getLogger('examples.artist_discography')
logging.basicConfig(level='INFO')


def get_args():
    parser = argparse.ArgumentParser(description='Shows albums and tracks for '
                                     'given artist')
    parser.add_argument('-a', '--artist', required=True,
                        help='Name of Artist')
    return parser.parse_args()


def get_artist(name):
    results = sp.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    return items[0] if items else None


def show_album_tracks(album):
    tracks = []
    results = sp.album_tracks(album['id'])
    tracks.extend(results['items'])
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    for i, track in enumerate(tracks):
        logger.info(f'{i + 1}. {track["name"]}')


def show_artist_albums(artist):
    albums = []
    results = sp.artist_albums(artist['id'], album_type='album')
    albums.extend(results['items'])
    while results['next']:
        results = sp.next(results)
        albums.extend(results['items'])
    logger.info(f'Total albums: {len(albums)}')
    unique = set()  # skip duplicate albums
    for album in albums:
        name = album['name'].lower()
        if name not in unique:
            logger.info(f'ALBUM: {name}')
            unique.add(name)
            show_album_tracks(album)


def show_artist(artist):
    logger.info(f'===={artist["name"]}====')
    logger.info(f'Popularity: {artist["popularity"]}')
    if len(artist['genres']) > 0:
        logger.info(f"Genres: {', '.join(artist['genres'])}")


def main():
    args = get_args()
    artist = get_artist(args.artist)
    show_artist(artist)
    show_artist_albums(artist)


if __name__ == '__main__':
    client_credentials_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    main()
