import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load the conversation dataset
def load_conversation(file_path, encoding="utf-8"):
    df = pd.read_csv(file_path, encoding=encoding)
    return df

# Train the chatbot model
def train_chatbot(conversation_df):
    corpus = conversation_df['question'] + ' ' + conversation_df['answer']
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus)
    similarity_matrix = cosine_similarity(tfidf_matrix)
    return vectorizer, similarity_matrix

# Simple chatbot with enhanced contextual understanding
def simple_chatbot(conversation_df, user_input, vectorizer, similarity_matrix, conversation_history):
    if user_input:
        # Add the user's input to the conversation history
        conversation_history.append({"User": user_input})
        
        # Retrieve the most relevant response based on cosine similarity
        user_input_tfidf = vectorizer.transform([user_input])
        similarity_scores = cosine_similarity(user_input_tfidf, vectorizer.transform(conversation_df['question'])).flatten()
        most_similar_index = similarity_scores.argmax()
        bot_response = conversation_df['answer'][most_similar_index]
        
        # Add the bot's response to the conversation history
        conversation_history[-1]["Bot"] = bot_response
        
        # Display the conversation history in a conversational format
        for exchange in conversation_history:
            if "User" in exchange:
                st.text(f"You: {exchange['User']}")
            if "Bot" in exchange:
                st.text(f"Bot: {exchange['Bot']}")
        
        # Clear user input after submission
        user_input = st.text_input("You:", key=f"user_input_{len(conversation_history)}")

        # Recursively call the chatbot function to continue the conversation
        simple_chatbot(conversation_df, user_input, vectorizer, similarity_matrix, conversation_history)

def main():
    st.title("Simple Chatbot: Enhanced Contextual Understanding")

    st.write(
        "A simple chatbot with enhanced contextual understanding can better grasp the nuances and details of a conversation. It recognizes greetings, expressions of gratitude, and responds accordingly. Additionally, it leverages a dataset to provide relevant answers to user queries."
    )

    conversation_path = 'Conversation.csv'
    conversation_encoding = "utf-8"
    conversation_df = load_conversation(conversation_path, encoding=conversation_encoding)

    vectorizer, similarity_matrix = train_chatbot(conversation_df)

    # Initialize conversation history
    conversation_history = []

    user_input = st.text_input("You:", key="user_input")
    simple_chatbot(conversation_df, user_input, vectorizer, similarity_matrix, conversation_history)

if __name__ == "__main__":
    main()










