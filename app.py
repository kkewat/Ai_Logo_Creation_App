import streamlit as st
import requests
import speech_recognition as sr
from PIL import Image
from io import BytesIO

# Function to handle speech recognition
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening...")
        audio_data = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio_data)
            st.success(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            st.error("Could not understand audio.")
            return ""
        except sr.RequestError as e:
            st.error(f"Error fetching results from Google Speech Recognition service: {e}")
            return ""

# Function to generate image from prompt
def generate_image(prompt):
    url = "https://api.limewire.com/api/image/generation"
    payload = {
        "prompt": prompt,
        "aspect_ratio": "1:1"
    }
    headers = {
        "Content-Type": "application/json",
        "X-Api-Version": "v1",
        "Accept": "application/json",
        "Authorization": "Bearer lmwr_sk_75uGGIdjNl_jM6ZZ6GEbLcG2jxyLxdMANECcfjozGx7Nh7W1"
    }

    response = requests.post(url, json=payload, headers=headers)
    data = response.json()
    if 'data' in data and len(data['data']) > 0:
        asset_url = data['data'][0].get('asset_url')
        if asset_url:
            return asset_url
        else:
            st.error("The 'asset_url' key was not found in the data.")
            return None
    else:
        st.error("No data received from the API.")
        return None

# Streamlit app layout
st.title("AI Image Generator")

col1, col2 = st.columns([4, 1])
with col1:
    prompt = st.text_input("Enter your prompt:")
with col2:
    if st.button("🎤"):
        speech_text = recognize_speech()
        if speech_text:
            st.session_state.prompt = speech_text
            prompt = speech_text

if st.button("Submit"):
    if prompt:
        image_url = generate_image(prompt)
        if image_url:
            response = requests.get(image_url)
            img = Image.open(BytesIO(response.content))
            st.image(img, caption=prompt)
    else:
        st.error("Please enter a prompt.")
