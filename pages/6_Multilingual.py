
import os
import streamlit as st
from translate import Translator as GoogleTranslator
import requests

# Function to translate text using Gemini Translate API
def translate_with_gemini(input_text, target_language="hi"):
    # Retrieve Gemini API key from environment variable
    gemini_api_key = os.getenv("GEMINI_API_KEY")

    # Set endpoint and parameters for Gemini Translate API request
    endpoint = "https://api.gemini.yahoo.com/v1/gtranslate"
    params = {
        "q": input_text,
        "target": target_language,
        "api_key": gemini_api_key
    }

    # Make request to Gemini Translate API
    response = requests.get(endpoint, params=params)

    # Check if request was successful
    if response.status_code == 200:
        translated_text = response.json()["output"]
        return translated_text
    else:
        return None

def main():
    # Set the title and subheading
    st.title("Multilingual Model")
    st.subheader("Introduction")

    # Display introductory text
    st.write(
        "A multilingual model is like a smart computer program that can understand and work with different languages. When some languages or dialects are not given enough attention or included in the program, it can cause problems. These problems may include the program behaving unfairly or not working well when dealing with specific language situations."
    )
    st.markdown(
        f"<div style='text-align: left;'><b> Aim : This code implements a simple multilingual model using Streamlit and the Translator. The goal is to demonstrate a basic translation capability between English and Hindi, as well as other languages.</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        f"<div style='text-align: left;'><br>[ Reference : hi = Hindi-India , es = Español-Spanish , mr = Marathi-India , gu = Gujrati-India ]<br> <br></div>",
        unsafe_allow_html=True
    )

    # Create an input text box for user input
    user_input = st.text_input("Enter a sentence (English):", "")

    # Create a selectbox for choosing the target language
    target_language = st.selectbox("Select target language:", ["Hindi", "Marathi", "Spanish", "Gujarati"])

    # Check if the user has entered a sentence and selected a target language
    if user_input and target_language:
        # Translate the input text using Gemini Translate API
        translated_text = translate_with_gemini(user_input, target_language[:2].lower())

        # Display the translated text
        st.write(f"Translated Text ({target_language}): {translated_text}")

if __name__ == "__main__":
    main()




