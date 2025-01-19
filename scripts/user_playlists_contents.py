# Shows a user's playlists (need to be authenticated via oauth)

import spotipy
from spotipy.oauth2 import SpotifyOAuth


def show_tracks(results):
    for i, item in enumerate(results['items']):
        track = item['track']
        print(f"   {i} {track['artists'][0]['name']:>32.32} {track['name']}")


if __name__ == '__main__':
    scope = 'playlist-read-private'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    playlists = sp.current_user_playlists()
    user_id = sp.me()['id']

    for playlist in playlists['items']:
        if playlist['owner']['id'] == user_id:
            print()
            print(playlist['name'])
            print('  total tracks', playlist['tracks']['total'])

            tracks = sp.playlist_items(playlist['id'], fields="items,next", additional_types=('tracks', ))
            show_tracks(tracks)

            while tracks['next']:
                tracks = sp.next(tracks)
                show_tracks(tracks)
