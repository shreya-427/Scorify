#TO RUN APP, RUN FOLLWING COMMAND IN TERMINAL: python -m streamlit run src/app.py
# imports Steamlit library into our program
import streamlit as st
import tempfile
import os                                # NEW: draws MusicXML as sheet music
from score import create_score
from models import QuantizedNote
from pipeline import run_pipeline
import base64
from pathlib import Path

st.set_page_config(
    page_title="Scorify",
    page_icon="🎵",
    layout="wide"
)

# Load galaxy banner image
image_path = Path(__file__).resolve().parent / "assets" / "galaxy_banner.jpg"

with open(image_path, "rb") as image_file:
    encoded_image = base64.b64encode(image_file.read()).decode()

#add a banner
st.markdown(
    f"""
<style>
.scorify-banner {{
    background-image:
        linear-gradient(
            rgba(10, 9, 25, 0.25),
            rgba(10, 9, 25, 0.25)
        ),
        url("data:image/jpeg;base64,{encoded_image}");

    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;

    padding: 25px 40px;
    color: white;
    width: 100%;
    box-sizing: border-box;
}}

.scorify-title {{
    font-size: 44px;
    font-weight: 900;
    line-height: 1.1;
    margin: 0;
    color: white;
}}

.scorify-subtitle {{
    font-size: 16px;
    margin-top: 5px;
    color: white;
}}

/* Match the heights of the Settings and Upload cards */
.st-key-settings_container,
.st-key-upload_container {{
    min-height: 380px;
}}

.st-key-generate_button button {{
    height: 185px;
    box-sizing: border-box;
}}

.st-key-download_button button {{
    height: 185px;
    box-sizing: border-box;
}}

.block-container {{
    padding-top: 4rem;
    max-width: 1500px;
}}
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
    [1.3, 1.8, 1.1],
    gap="large"
)

# LEFT COLUMN: SETTINGS
with settings_col:
    with st.container(border=True, key="settings_container"):
        st.subheader("Settings", anchor=False)

        # Score name input
        score_name = st.text_input(
            "Score Name", value="Untitled"
        )

        # Composer name input
        composer_name = st.text_input(
            "Composer Name", value="Name"
        )

        # BPM input
        bpm = st.number_input(
            "Tempo (BPM)",
            min_value=40,
            max_value=240,
            value=120
        )

# MIDDLE COLUMN: AUDIO UPLOAD
with upload_col:
    with st.container(border=True, key="upload_container"):
        st.subheader("Upload Audio", anchor=False)

        uploaded_file = st.file_uploader(
            "Upload an audio file in .wav or .mp3 format",
            type=["wav", "mp3"]
        )

        # Display uploaded audio
        if uploaded_file is not None:
            st.success("Audio file has been uploaded successfully!")
            st.audio(uploaded_file)


# RIGHT COLUMN: ACTIONS
with action_col:
    generate_button = st.button(
        "Generate Sheet Music",
        use_container_width=True,
        type="secondary",
        key="generate_button"
    )

    st.download_button(
        label="Download Score (MusicXML)",
        data=st.session_state.musicxml_data or b"",
        file_name="scorify_sheet_music.musicxml",
        mime="application/vnd.recordare.musicxml+xml",
        use_container_width=True,
        disabled=st.session_state.musicxml_data is None,
        key="download_button"
    )


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
        st.rerun()
