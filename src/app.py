#TO RUN APP, RUN FOLLWING COMMAND IN TERMINAL: python -m streamlit run src/app.py
# imports Steamlit library into our program
import streamlit as st
import tempfile
import os
from score import create_score
from models import QuantizedNote
from pipeline import run_pipeline


#add a banner
st.markdown(
"""
<style>
.scorify-banner {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 120px;
    box-sizing: border-box;
    z-index: 1000000;
    background-color: #4B3F72;
    color: white;
    text-align: left;
    padding: 15px 40px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.scorify-title {
    font-size: 44px;
    font-weight: 900;
    line-height: 1.1;
    margin: 0;
}

.scorify-subtitle {
    font-size: 16px;
    margin-top: 5px;
}

.block-container {
    padding-top: 9rem;
}
</style>

<div class="scorify-banner">
    <div class="scorify-title">SCORIFY</div>
    <div class="scorify-subtitle">
        Turn your recordings into editable sheet music
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# # Page title and description
# st.title("Scorify")
# st.write("Welcome to Scorify! Turn your audio recordings into editable sheet music!")

#add a banner

# Initialize Session State
# This stores the generated MusicXML file between Streamlit reruns
if "musicxml_data" not in st.session_state:
    st.session_state.musicxml_data = None

st.title("Welcome to Scorify!")
st.write(
    "Upload your audio recording and provide a BPM, title, and composer "
    "to generate editable sheet music in MusicXML format."
)

settings_col, upload_col, action_col = st.columns(
    [1.2, 1.6, 0.9],
    gap="large"
)

# Audio file uploader
uploaded_file = st.file_uploader(
    "Upload an audio file in .wav or .mp3 format",
    type=["wav", "mp3"]
)

#score name input
score_name = st.text_input(
    "Score Name", value="Untitled")

#composer name input
composer_name = st.text_input("Composer Name", value="Name")

# BPM input
bpm = st.number_input(
    "Tempo (BPM)",
    min_value=40,
    max_value=240,
    value=120
)

# Display uploaded audio
if uploaded_file is not None:
    st.success("Audio file has been uploaded successfully!")
    st.audio(uploaded_file)

# Generate sheet music button
generate_button = st.button("Generate Sheet Music")

if generate_button:
    if uploaded_file is None:
        st.error("No audio file uploaded")
    else:
        with st.spinner("Generating sheet music..."):

            # Create the musical score

            suffix = os.path.splitext(uploaded_file.name)[1]

            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
                temp_file.write(uploaded_file.getvalue())
                temp_path = temp_file.name

            try:
                result = run_pipeline(temp_path, bpm,score_name,composer_name)
            finally:
                os.remove(temp_path)

            # Export the score as MusicXML
            #result.write("musicxml", fp="test_score.xml")

            # Read the generated file into memory
            with open("test_score.xml", "rb") as f:
                st.session_state.musicxml_data = f.read()

        st.success("Score generated successfully!")

# Display the download button whenever a score is available
if st.session_state.musicxml_data is not None:
    st.download_button(
        label="Download Sheet Music",
        data=st.session_state.musicxml_data,
        file_name="scorify_sheet_music.musicxml",
        mime="application/vnd.recordare.musicxml+xml"
    )
