#TO RUN APP, RUN FOLLWING COMMAND IN TERMINAL: python -m streamlit run src/app.py
# imports Steamlit library into our program
import streamlit as st
import tempfile
import os
from score import create_score
from models import QuantizedNote
from pipeline import run_pipeline


# Page title and description
st.title("Scorify")
st.write("Welcome to Scorify! Turn your audio recordings into editable sheet music!")

# Initialize Session State
# This stores the generated MusicXML file between Streamlit reruns
if "musicxml_data" not in st.session_state:
    st.session_state.musicxml_data = None

# Audio file uploader
uploaded_file = st.file_uploader(
    "Upload an audio file in .wav or .mp3 format",
    type=["wav", "mp3"]
)

# BPM input
bpm = st.number_input(
    "Tempo (BPM)",
    min_value=40,
    max_value=240,
    value=120
)

# Lead-in time input
lead_in_s = st.number_input(
        "Lead-in Time (seconds)",
        min_value=0.0,
        max_value=3.0,
        value=0.0
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
                result = run_pipeline(temp_path, bpm, lead_in_s)
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