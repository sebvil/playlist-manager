import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import unicodedata

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
count = 0

def strip_accents(text):

    try:
        text = unicode(text, 'utf-8')
    except NameError: # unicode is a default on python 3
        pass

    text = unicodedata.normalize('NFD', text)\
           .encode('ascii', 'ignore')\
           .decode("utf-8")

    return str(text)

s = strip_accents('àéêöhello')



class Query:
    def __init__(self, search=None, album=None, artist=None, unique=False):
        self.search = search
        self.album = album
        self.artist = artist
        self.unique = unique
        print(self.unique)
        self.q = self.build_query()

    def build_query(self):
        query = None
        s = ''
        search = None
        if self.search:
            query = self.search

        album = None
        if self.album:
            if query:
                query = ' AND '.join((query, self.album))
            else:
                query = self.album

        artist = None
        if self.artist:
            if query:
                query = ' AND '.join((query, self.artist))
            else:
                query = self.artist

        return query

    def make_query(self):
        offset = 0
        track_names = {}
        query_results = []
        try:
            while results := sp.search(q=self.q, limit=50, offset=offset):
                offset += 50
                print(offset)
                print(results)
                if not results['tracks']['items']:
                    break
                for track in results['tracks']['items']:
                    temp = 0
                    track_id = track['id']

                    track_name = track['name']




                    artists_list = []
                    for artist in track['artists']:
                        artists_list.append(artist['name'])

                    if self.artist and self.artist.lower() not in (strip_accents(artist.lower()) for artist in artists_list):
                        continue
                    artists = ', '.join(sorted(artists_list))

                    if self.unique and strip_accents(track_name.lower()) in track_names.keys():
                        if artists in track_names[strip_accents(track_name.lower())]:
                            continue
                        else:
                            track_names[strip_accents(track_name.lower())].append(artists)

                    elif self.unique:
                        track_names[strip_accents(track_name.lower())] = [artists]


                    album = track['album']['name']

                    if self.album and self.album.lower() not in strip_accents(album.lower()):
                        continue


                    preview_url = track['preview_url']

                    qr = QueryResult(track_id, track_name, artists, album, preview_url)
                    query_results.append(qr)
        #         for t in sorted(track_names.keys()):
        #             print(t, track_names[t])
        except spotipy.exceptions.SpotifyException:
            return query_results

        return query_results


class QueryResult:
    def __init__(self, track_id, track, artist, album, preview_url, selected=False):
        self.track_id = track_id
        self.track = track
        self.artist = artist
        self.album = album
        self.preview_url = preview_url
        self.selected = selected

    def __repr__(self):
        return f'{self.track_id},{self.track},{self.artist},{self.album},{self.preview_url},{self.selected}'


"""
if __name__ == '__main__':
    i = 0
    song_dict = {}
    while True:
        results = sp.search(q='artist:melendi NOT artist:melendiz', limit=50, offset=i)
        for song in results['tracks']['items']:
            # print(count, song['name'], end=',')
            count += 1
            artists = []
            for artist in song['artists']:
                # print(artist['name'], end=',')
                artists.append(artist['name'])

            if song['name'] not in song_dict:
                song_dict[song['name']] = artists
            elif song_dict[song['name']] != artists:
                j = 1
                while song['name'] + str(j) in song_dict and song_dict[song['name'] + str(j)] != artists :
                    j += 1
                    print(j)
                song_dict[song['name'] + str(j)] = artists


            # print()
        i += 50
        if len(results['tracks']['items']) < 50:
            break
    i = 1
    for song in sorted(song_dict.keys()):
        print(i, song, song_dict[song])
        i += 1
"""
