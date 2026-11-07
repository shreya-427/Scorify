# imports Steamlit library into our program
import streamlit as st #at st gives steamlit a nickname of st

st.title("Scorify") #creates title text
st.write("Welcome to Scorify! Turn your audio recordings into ediable sheet music!") #creates sub text

#creating the place to upload the audio file
uploaded_file = st.file_uploader("Upload an audio file of .wav or .mp3 formate", type=["wav", "mp3"])

# creates a place for user to input BPM
bpm = st.number_input("Tempo (BPM)", min_value=40, max_value=240, value=120)

if uploaded_file is not None:
    st.success("Audio file has been uploaded successfully!") #creates a success message if the file is uploaded
    st.audio(uploaded_file) #allows users to listen to their recoreding inside of webpage

generate_button = st.button("Generate Sheet Music") #creates button
if generate_button:
    if uploaded_file is None:
        st.error("No audio file uploaded")
    else:
        st.spinner("Generating sheet music...")
    

