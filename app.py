import streamlit as st
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from googleapiclient.discovery import build

nltk.download('vader_lexicon')

def analyze_sentiment(text):
    sid = SentimentIntensityAnalyzer()
    sentiment_scores = sid.polarity_scores(text)

    # Interpret the sentiment score
    if sentiment_scores['compound'] >= 0.05:
        return 'positive'
    elif sentiment_scores['compound'] <= -0.05:
        return 'negative'
    else:
        return 'neutral'

# Define functions for sentiment analysis and model prediction
def predict_sentiment(video_id):
    # API key and YouTube Data API service
    API_KEY = "AIzaSyD74cfUIsVfvXlfnuSVV7sg_cwulqehRMc"
    youtube = build("youtube", "v3", developerKey=API_KEY)

    # Fetch comments
    comments_list = []
    next_page_token = None
    while True:
        request = (
            youtube.commentThreads()
            .list(
                part="snippet",
                videoId=video_id,
                maxResults=100,
                pageToken=next_page_token,
            )
            .execute()
        )
        # Use the correct key for comment text
        comments_list += [c["snippet"]["topLevelComment"]["snippet"]["textOriginal"] for c in request["items"]]
        next_page_token = request.get("nextPageToken")
        if not next_page_token:
            break

    # Predict sentiment using sentiment analysis function
    predicted_sentiments = [analyze_sentiment(comment) for comment in comments_list]

    # Count and calculate percentages
    positive_count = sum(sentiment == 'positive' for sentiment in predicted_sentiments)
    negative_count = sum(sentiment == 'negative' for sentiment in predicted_sentiments)
    neutral_count = sum(sentiment == 'neutral' for sentiment in predicted_sentiments)
    total_count = len(comments_list)
    positive_percentage = (positive_count / total_count) * 100
    negative_percentage = (negative_count / total_count) * 100
    neutral_percentage = (neutral_count / total_count) * 100

    # Return results
    return {
        "positive_percentage": positive_percentage,
        "negative_percentage": negative_percentage,
        "neutral_percentage": neutral_percentage,
    }

# Set page title
st.title("YouTube Comment Sentiment Analysis")

# Input for YouTube video ID
video_id = st.text_input("Enter YouTube Video ID:")

if st.button('Predict'):

# Check if the video ID is provided
 if video_id:
    # Perform sentiment analysis
    results = predict_sentiment(video_id)

    # Display results
    st.write(f"Positive comments: {results['positive_percentage']:.2f}%")
    st.write(f"Negative comments: {results['negative_percentage']:.2f}%")
    st.write(f"Neutral comments: {results['neutral_percentage']:.2f}%")

    # Example: Embed a YouTube video based on the video ID
    st.video(f"https://www.youtube.com/watch?v={video_id}")

