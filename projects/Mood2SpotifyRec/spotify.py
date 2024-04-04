# spotify stuff goes here: aka spotify calls, playlist creation, music matching, etc.

import SeedData
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth


class SpotifyTools:
    def __init__(self, client_id, client_secret):
        if client_id is None or client_secret is None:
            raise ValueError(
                "Follow README tutorial to create a Spotify Developer account and get the client_id and client_secret."
            )
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = self.get_access_token()
        self.sp = spotipy.Spotify(auth=self.access_token)
        self.scope = "playlist-read-private playlist-read-collaborative playlist-modify-private playlist-modify-public"
        self.sp_oauth = SpotifyOAuth(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri="http://localhost:8888/callback",
            scope=self.scope,
        )
        self.sp_authenticated = spotipy.Spotify(auth_manager=self.sp_oauth)
        self.user_id = self.set_user_id()

    def set_user_id(self):
        """Set the user id for the authenticated user

        Returns:
            str: user id
        """
        sp_user_info = self.sp_authenticated.current_user()
        sp_user_id = sp_user_info["id"]
        return sp_user_id

    def get_access_token(self):
        """Get access token for spotify API call

        Returns:
            text (str): spotify access token
        """
        auth_url = "https://accounts.spotify.com/api/token"
        auth_response = requests.post(
            auth_url,
            {
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            },
        )
        auth_response_data = auth_response.json()
        return auth_response_data.get("access_token")

    # def get_audio_features(self, track_id):
    #     base_url = "https://api.spotify.com/v1/audio-features/"
    #     headers = {
    #         "Authorization": f"Bearer {self.access_token}",
    #     }
    #     response = requests.get(f"{base_url}{track_id}", headers=headers)
    #     data = response.json()
    #     # Filter the response to include only the desired attributes
    #     filtered_data = {
    #         k: v
    #         for k, v in data.items()
    #         if k in ("valence", "energy", "instrumentalness", "loudness", "tempo")
    #     }
    #     return filtered_data

    # def search_artist_details(self, artist_name):
    #     # Search for the artist
    #     result = self.sp.search(q=artist_name, type="artist")
    #     items = result["artists"]["items"]
    #     if not items:
    #         return None

    #     # Assuming we take the first artist and their first image
    #     artist_info = {
    #         "id": items[0]["id"],
    #         "name": items[0]["name"],
    #         "image_url": items[0]["images"][0]["url"] if items[0]["images"] else None,
    #     }

    #     return artist_info

    def get_available_genre(self):
        """Get available genres for recommendations
        Returns:
            _type_: _description_
        """
        sp = spotipy.Spotify(auth=self.access_token)
        recommended_genre_seeds = sp.recommendation_genre_seeds()
        return recommended_genre_seeds

    def get_tracks_recommendations(self, seed_data):
        """Tracks recommendations using Spotify API based on seed data

        Args:
            seed_data (dict): eed data provided by the LLM model

        Returns:
            dict: recommended tracks
        """
        recommended_tracks = self.sp.recommendations(
            limit=10,
            seed_genres=seed_data.seed_genres,
            seed_artists=seed_data.seed_artists,
            target_valence=seed_data.target_valence,
            target_energy=seed_data.target_energy,
            target_danceability=seed_data.target_danceability,
            target_acousticness=seed_data.target_acousticness,
        )
        return recommended_tracks

    # TODO: remove when done
    def get_test_track_recommendation(self):
        testSeedData = SeedData.SeedData().get_test_seed_data()
        return self.get_tracks_recommendations(testSeedData)
        # print(recommended_track)
        # print(type(recommended_track))

    def add_recommend_tracks_to_playlist(self, playlist_name, seed_data):
        """create a playlist in user's spotify account and add recommended tracks to it

        Args:
            playlist_name (str): name the playlist
            seed_data (dict): seed data provided by the LLM model

        Returns:
            str: generated playlist id
        """
        recommended_tracks = self.get_tracks_recommendations(seed_data)
        track_ids = [track["id"] for track in recommended_tracks["tracks"]]
        playlist = self.sp_authenticated.user_playlist_create(
            user=self.user_id, name=playlist_name, public=False
        )
        playlist_id = playlist["id"]
        self.sp_authenticated.user_playlist_add_tracks(
            user=self.user_id, playlist_id=playlist_id, tracks=track_ids
        )
        return playlist_id
