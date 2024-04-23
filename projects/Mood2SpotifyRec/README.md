# Mood2SpotifyRec

Quick app to use the user's mood input as generation data to a Spotify playlist.

# Setup

Have poetry installed. Run

```terminal
poetry install
```

## Get spotify client id and secret

follow this tutorial: https://support.heateor.com/get-spotify-client-id-client-secret/

> Note that for the redirect URI, enter "http://localhost:8888/callback"

## Running the webapp

in command line, export your client id and secret

```terminal
export SPOTIPY_CLIENT_ID="your client id goes here"
export SPOTIPY_CLIENT_SECRET="your client secret goes here"
```

then run

```terminal
streamlit run main.py
```
