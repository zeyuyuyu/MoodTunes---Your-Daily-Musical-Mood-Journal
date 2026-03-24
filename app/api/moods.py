import os
import openai
from flask import Blueprint, request, jsonify
from app.models import Mood

api = Blueprint('moods', __name__, url_prefix='/api/moods')

openai.api_key = os.environ.get('OPENAI_API_KEY')

@api.route('/', methods=['POST'])
def create_mood():
    data = request.get_json()
    text = data['text']
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Analyze the sentiment of the following text: {text}",
        max_tokens=1,
        n=1,
        stop=None,
        temperature=0.5,
    )
    sentiment = response.choices[0].text.strip()
    mood = Mood(text=text, sentiment=sentiment)
    mood.save()
    return jsonify({
        'id': mood.id,
        'text': mood.text,
        'sentiment': mood.sentiment,
        'created_at': mood.created_at.isoformat()
    })