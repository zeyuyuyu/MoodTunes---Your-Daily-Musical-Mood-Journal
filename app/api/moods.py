import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model

SENTIMENT_MODEL_PATH = os.getenv('SENTIMENT_MODEL_PATH')

class MoodSentimentAnalyzer:
    def __init__(self):
        self.sentiment_model = load_model(SENTIMENT_MODEL_PATH)

    def analyze_sentiment(self, mood_text):
        sentiment_input = np.array([mood_text])
        sentiment_scores = self.sentiment_model.predict(sentiment_input)
        return sentiment_scores[0]

class MoodAPI:
    def __init__(self):
        self.sentiment_analyzer = MoodSentimentAnalyzer()

    def create_mood_entry(self, user_id, mood_text):
        sentiment_scores = self.sentiment_analyzer.analyze_sentiment(mood_text)
        # Save mood entry with sentiment scores to the database
        return {
            'user_id': user_id,
            'mood_text': mood_text,
            'sentiment_scores': sentiment_scores.tolist()
        }
