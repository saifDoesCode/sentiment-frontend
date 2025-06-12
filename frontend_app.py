import streamlit as st
import requests  # The library used to send requests to your API

# --- Configuration ---
# IMPORTANT: Replace this placeholder with the actual URL of your deployed Render API
# It should look something like: https://your-app-name.onrender.com/predict
API_URL = "https://sentiment-app-86qk.onrender.com/predict" 


# --- User Interface ---
st.title("💬 ToneTracker")
st.write(
    "Enter a message (like a text, tweet, or chat) to see if its tone is "
    "**Positive** or **Negative**."
)

# User input text area
user_input = st.text_area("Enter your message here:", height=120)

# Analyze button
if st.button("Analyze Sentiment"):
    # Check if the user has entered any text
    if user_input:
        # Show a spinner while we wait for the API's response
        with st.spinner('Contacting the AI model...'):
            try:
                # The data to send to the API, in a JSON format
                payload = {"text": user_input}
                
                # Make the POST request to our FastAPI backend on Render
                response = requests.post(API_URL, json=payload)
                
                # Check if the request was successful (status code 200)
                if response.status_code == 200:
                    prediction_data = response.json()
                    sentiment = prediction_data['sentiment']
                    confidence = prediction_data['confidence']
                    
                    # Display the results
                    st.subheader("Analysis Result")
                    if sentiment == 'positive':
                        st.success(f"Sentiment: Positive 😊")
                    else:
                        st.error(f"Sentiment: Negative 😠")

                    st.subheader("Prediction Confidence")
                    st.write(f"Negative: {confidence['negative']}%")
                    st.write(f"Positive: {confidence['positive']}%")
                else:
                    # Show an error if the API returned a non-200 status code
                    st.error(f"Error: Could not get a prediction from the API. Status code: {response.status_code}")
                    st.write(response.text) # Display the detailed error from the API

            except requests.exceptions.RequestException as e:
                # Show an error if there's a problem connecting to the API
                st.error(f"An error occurred while trying to connect to the API: {e}")
    else:
        # Show a warning if the user clicks the button with no text
        st.warning("Please enter a message to analyze.")

st.markdown("---")
st.write("Developed by Saif.")
st.write("The dataset used for training had **1.6 Million rows of data.**")
st.write("AI model is trained on the Sentiment140 dataset.")
st.write("UI by Streamlit | AI Model is hosted on Render")