import streamlit as st
import streamlit.components.v1 as components
import spotify
import SeedData

st.title("Mood 2 Spotify Recommendation")

# Inputs for Client ID and Client Secret
client_id = st.text_input("Client ID", "")
client_secret = st.text_input("Client Secret", "")
sp = spotify.SpotifyTools(client_id, client_secret)
access_token = sp.get_access_token()


# Section for Audio Features
# st.subheader("Get Audio Features")
# track_id = st.text_input("Spotify Track ID", "")
# if st.button("Get Audio Features"):
#     if not client_id or not client_secret or not track_id:
#         st.warning("Please fill in all fields for audio features")
#     else:
#         if access_token:
#             analysis = sp.get_audio_features(track_id)
#             st.json(analysis)
#         else:
#             st.error("Failed to retrieve access token for audio features")

# Section for Artist Search
# st.subheader("Search for an Artist")
# artist_name = st.text_input("Artist Name", "")
# if st.button("Search Artist"):
#     if not client_id or not client_secret or not artist_name:
#         st.warning("Please fill in all fields.")
#     else:
#         artist_info = sp.search_artist_details(artist_name)
#         if artist_info and artist_info["image_url"]:
#             st.image(artist_info["image_url"], caption=f"Artist: {artist_info['name']}")
#         else:
#             st.error("Artist not found or has no images.")

# Test for available genres
# st.subheader("Available Genres: ")
# if st.button("Get Recommendations"):
#     if not client_id or not client_secret:
#         st.warning("Please fill in all fields.")
#     else:
#         if access_token:
#             recommended_genre_seeds = sp.get_genre_recommendations("indie")
#             st.write(f"{recommended_genre_seeds}")
#         else:
#             st.error("Failed to retrieve access token for recommendations")

# Section for track recommendations
st.subheader("Get TEST Track Recommendations")
test_seed_data = SeedData.SeedData().get_test_seed_data()
st.write(test_seed_data)
if st.button("Get TEST Tracks Recommendations"):
    if not client_id or not client_secret:
        st.warning("Please fill in all fields.")
    else:
        if access_token:
            recommended_tracks = sp.get_test_track_recommendation()
            track_uris = [track["uri"] for track in recommended_tracks["tracks"]]
            # Display the tracks as clickable links
            for track in recommended_tracks["tracks"]:
                track_name = track["name"]
                artists = ", ".join(
                    artist["name"] for artist in track["album"]["artists"]
                )
                spotify_url = track["external_urls"]["spotify"]
                st.write(f"[{track_name} by {artists}]({spotify_url})")

        else:
            st.error("Failed to retrieve access token for recommendations")

# Show embed TEST recommendation playlist
if st.button("Show playlist"):
    user_id = sp.user_id
    playlist_id = sp.add_recommend_tracks_to_playlist(
        "Mood2Spotify Playlist", test_seed_data
    )
    # Your playlist embed URL
    playlist_embed_url = "https://open.spotify.com/embed/playlist/" + playlist_id
    # Embed the playlist using an iframe
    components.html(
        f"""<iframe src="{playlist_embed_url}" width=100% height=700 frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>""",
        height=700,
    )
