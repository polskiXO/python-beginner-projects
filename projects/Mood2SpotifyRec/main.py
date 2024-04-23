import streamlit as st
import streamlit.components.v1 as components
import spotify
import SeedData
import os
from llm import Mood2SpotifyRec
from dotenv import load_dotenv
from PIL import Image


# Load environment variables
load_dotenv()

# Streamlit page background
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQlo3P16G9dPsRjdEhx77zlzr2idJqnXZpLuQ90xNYrpQ&s");
background-size: cover;
background-position: center center;
background-repeat: no-repeat;
background-attachment: local;
}}
[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# =========================================================================================================
# Logo and Navigation
st.title("Mood 2 Spotify Recommendation")
mood2spotifyrec_logo = Image.open(
    "resources/Mood2SpotifyRec_Logov2-fotor-bg-remover-20240423143851.png"
)
st.image(mood2spotifyrec_logo, width=300)
# change the size of the logo and center


# Inputs for Client ID and Client Secret
client_id = os.getenv("SPOTIPY_CLIENT_ID")
client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
sp = spotify.SpotifyTools(client_id, client_secret)
access_token = sp.get_access_token()

# =========================================================================================================
# The user input and recommendation section
converter = Mood2SpotifyRec(google_api_key=os.getenv("GOOGLE_API_KEY"))
# User input for mood
st.subheader("Enter your mood:")
mood = st.text_input("Mood", "")

# Output
if st.button("Get Tracks Recommendations:"):
    # Validate inputs
    if not client_id or not client_secret:
        st.warning("Please fill in all fields.")
    if not mood.strip():
        st.write("*Please complete the missing fields.")
    else:
        st.header("Output")
        st.write("This is the Spotify metrics based on your mood:")
        mood_text = mood.strip()
        metrics = converter.convert(mood_text)
        st.write(f"`{metrics}`")  # Display metrics in code block
        rec_seed_data = SeedData.SeedData().to_seed_data(metrics)
        user_id = sp.user_id
        playlist_id = sp.add_recommend_tracks_to_playlist(
            "Mood2Spotify Playlist", rec_seed_data
        )
        # Your playlist embed URL
        playlist_embed_url = "https://open.spotify.com/embed/playlist/" + playlist_id
        # Embed the playlist using an iframe
        components.html(
            f"""<iframe src="{playlist_embed_url}" width=100% height=700 frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>""",
            height=700,
        )


# =========================================================================================================
# API test and LLM suggestion test
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

# Spotify recommendation API test
# st.subheader("Get TEST Track Recommendations")
# test_seed_data = SeedData.SeedData().get_test_seed_data()
# st.write(test_seed_data)
# if st.button("Get TEST Tracks Recommendations"):
#     if not client_id or not client_secret:
#         st.warning("Please fill in all fields.")
#     else:
#         if access_token:
#             recommended_tracks = sp.get_test_track_recommendation()
#             track_uris = [track["uri"] for track in recommended_tracks["tracks"]]
#             # Display the tracks as clickable links
#             for track in recommended_tracks["tracks"]:
#                 track_name = track["name"]
#                 artists = ", ".join(
#                     artist["name"] for artist in track["album"]["artists"]
#                 )
#                 spotify_url = track["external_urls"]["spotify"]
#                 st.write(f"[{track_name} by {artists}]({spotify_url})")

#         else:
#             st.error("Failed to retrieve access token for recommendations")

# Show embed TEST recommendation playlist
# if st.button("Show playlist"):
#     user_id = sp.user_id
#     playlist_id = sp.add_recommend_tracks_to_playlist(
#         "Mood2Spotify Playlist", test_seed_data
#     )
#     # Your playlist embed URL
#     playlist_embed_url = "https://open.spotify.com/embed/playlist/" + playlist_id
#     # Embed the playlist using an iframe
#     components.html(
#         f"""<iframe src="{playlist_embed_url}" width=100% height=700 frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>""",
#         height=700,
#     )


# =========================================================================================================
# Sidebar
st.sidebar.header("About")
st.sidebar.markdown(
    """
    A project by [polskiXO](https://github.com/polskiXO) and [menamerai](https://github.com/menamerai) for EECE3092.
    
    Mood2SpotifyRec is made using Google Gemini LLM to generate seed param based on user input mood to feed into Spotify API recommendation API for playlist generation. 
    """
)

st.sidebar.header("Resources")
st.sidebar.markdown(
    """
- [GitHub Repository](https://github.com/polskiXO/python-beginner-projects/tree/2-natlang2latex-project/projects/Mood2SpotifyRec)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [LaTeX Documentation](https://www.latex-project.org/help/documentation/)
- [Google Gemini](https://ai.google.dev/)
- [EECE3092 Course](https://www.ece.mcgill.ca/~ece309/)
"""
)
