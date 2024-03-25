import os, streamlit as st
from PIL import Image


# Streamlit page background
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("https://i.postimg.cc/4xgNnkfX/Untitled-design.png");
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
natlang2latex_logo = Image.open("resources/NatLang2Latex_logo2_DallE.png")
st.image(natlang2latex_logo)

# Title
st.title("Natural Language to LaTeX")
st.write("This is a simple web app that converts natural language to LaTeX.")

# Input
st.header("Input")
input_text = st.text_area("Enter your mathematical natural language expression:")

# Output
if st.button("Convert to LaTeX"):
    # Validate inputs
    if not input_text.strip():
        st.write("*Please complete the missing fields.")
    else:
        st.header("Output")
        st.write("This is the LaTeX representation of your expression:")
        # TODO: Add the conversion logic here


# =========================================================================================================
# Sidebar
st.sidebar.header("About")
st.sidebar.markdown(
    """
    A project by [polskiXO](https://github.com/polskiXO) and [menamerai](https://github.com/menamerai) for EECE3092.
    
    NatLang2Latex is made using Google Gemini API to convert natural language to LaTeX and hosted on Streamlit. 
    """
)

st.sidebar.header("Resources")
st.sidebar.markdown(
    """
- [GitHub Repository](https://github.com/polskiXO/python-beginner-projects/tree/2-natlang2latex-project/projects/NatLang2Latex)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [LaTeX Documentation](https://www.latex-project.org/help/documentation/)
- [Google Gemini](https://ai.google.dev/)
- [EECE3092 Course](https://www.ece.mcgill.ca/~ece309/)
"""
)
