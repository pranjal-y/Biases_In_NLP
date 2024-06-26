import streamlit as st
from textblob import TextBlob
import pandas as pd

# Function to load dataset
def load_dataset(file_path, encoding="utf-8", nrows=None):
    df = pd.read_csv(file_path, encoding=encoding, nrows=nrows)
    return df

# Function to define exclusion list
def define_exclusion_list():
    # Define exclusion list containing words related to sensitive demographics
    exclusion_list = [
        "race", "ethnicity", "gender", "religion",
        "black", "white", "asian", "hispanic", "latino", "african",
        "indian", "native", "arab", "middle eastern",
        "male", "female", "man", "woman", "boy", "girl",
        "christian", "muslim", "hindu", "jewish", "buddhist",
        "straight", "gay", "lesbian", "bisexual", "transgender", "queer"
    ]
    return exclusion_list

# Function for sentiment analysis with masking exclusion list words
def perform_sentiment_analysis(user_input, exclusion_list):
    # Mask exclusion list words with a basic word
    for word in exclusion_list:
        user_input = user_input.replace(word, "person")

    # Perform sentiment analysis on the modified input
    analysis = TextBlob(user_input)
    sentiment = analysis.sentiment.polarity

    # Classify sentiment
    if sentiment > 0.1:  # Adjust the threshold as needed
        return "positive"
    elif sentiment < -0.1:  # Adjust the threshold as needed
        return "negative"
    else:
        # Additional check for negative sentiments in specific statements
        # Additional negative words for sentiment analysis
        negative_words = [
    "abhorrent", "abominable", "atrocious", "awful", "bad", "baneful", "base", "beastly", "brutal", "contemptible",
    "cursed", "deplorable", "despicable", "detestable", "dire", "disgusting", "dreadful", "execrable", "ghastly",
    "grim", "grisly", "gross", "hateful", "heinous", "horrendous", "horrible", "horrid", "infamous", "iniquitous",
    "loathsome", "lousy", "malevolent", "miserable", "nasty", "odious", "offensive", "opprobrious", "repellent",
    "repugnant", "reprehensible", "revolting", "rotten", "shocking", "sickening", "sinister", "sordid", "squalid",
    "ugly", "vile", "wicked", "wretched"
]


        if any(word in user_input.lower() for word in negative_words):  # Check for specific negative terms
            return "negative"
        else:
            return "neutral"


def main():
    # Set the title and subheading
    st.title("Sentiment Analysis: Misclassification and Unintended Consequences")
    st.subheader("Introduction")

    # Display introductory text
    st.write(
        "Sentiment analysis is a process that involves determining the emotional tone or sentiment expressed in a piece of text. Misclassification in sentiment analysis refers to instances where the model incorrectly predicts the sentiment of a text, leading to inaccurate results. Unintended consequences in sentiment analysis refer to unexpected outcomes or implications that may arise due to misclassifications, such as the dissemination of misinformation, biased insights, or the misinterpretation of user sentiments."
    )
    st.markdown(
        f"<div style='text-align: left;'><b> Aim :In this segment, we'll apply sentiment analysis to categorize sentences into positive, negative, or neutral classes.<br> </div>",
        unsafe_allow_html=True
    )
    # Create an input text box for user input
    user_input = st.text_area("Enter a statement:", "")

    # Define exclusion list
    exclusion_list = define_exclusion_list()

    # Load the dataset
    dataset_path = 'target.csv'
    dataset_encoding = "ISO-8859-1"  # Replace with the correct encoding

    # Add pagination to display a subset of the dataset
    page_size = st.slider("Select number of rows to display:", 1, 100, 10)
    current_page = st.number_input("Enter page number:", 1, value=1)

    start_idx = (current_page - 1) * page_size
    end_idx = start_idx + page_size

    dataset = load_dataset(dataset_path, encoding=dataset_encoding, nrows=end_idx)

    # Display the original dataset with pagination
    st.subheader("Original Data")
    st.dataframe(dataset[start_idx:end_idx])

    # Button to trigger sentiment analysis
    if st.button("Analyze"):
        # Perform sentiment analysis
        result = perform_sentiment_analysis(user_input, exclusion_list)

        # Display sentiment analysis result
        st.subheader("Sentiment Analysis Result:")
        st.write(f"Text: {user_input}")
        st.write(f"Predicted Sentiment: {result}")

    # Cautionary note
    st.subheader("Caution:")
    st.write(
        "This is a simple example app for demonstration purposes. It uses a basic sentiment analysis approach. "
        "In a real-world scenario, careful consideration, testing, and monitoring are required to mitigate risks."
    )

if __name__ == "__main__":
    main()



