from datetime import datetime, timedelta
from typing import List, Dict
from collections import Counter
import statistics

class MoodAnalyzer:
    def __init__(self):
        self.mood_scores = {
            'happy': 1.0,
            'excited': 0.8,
            'peaceful': 0.6,
            'neutral': 0.5,
            'melancholic': 0.3,
            'sad': 0.2,
            'angry': 0.1
        }
        
        self.genre_mapping = {
            'happy': ['pop', 'dance', 'funk'],
            'excited': ['rock', 'electronic', 'hip-hop'],
            'peaceful': ['ambient', 'classical', 'jazz'],
            'neutral': ['indie', 'folk', 'alternative'],
            'melancholic': ['blues', 'soul', 'indie'],
            'sad': ['classical', 'ambient', 'folk'],
            'angry': ['metal', 'punk', 'rock']
        }

class MoodAPI:
    def __init__(self):
        self.analyzer = MoodAnalyzer()
        self.moods_db = []  # In real implementation, this would be a database

    def log_mood(self, mood: str, timestamp: datetime, notes: str = None) -> Dict:
        """Log a new mood entry"""
        entry = {
            'mood': mood,
            'timestamp': timestamp,
            'notes': notes,
            'score': self.analyzer.mood_scores.get(mood, 0.5)
        }
        self.moods_db.append(entry)
        return entry

    def get_mood_trends(self, days: int = 7) -> Dict:
        """Analyze mood trends over specified period"""
        cutoff = datetime.now() - timedelta(days=days)
        recent_moods = [m for m in self.moods_db if m['timestamp'] >= cutoff]
        
        if not recent_moods:
            return {'error': 'No mood data available'}
            
        scores = [m['score'] for m in recent_moods]
        mood_counts = Counter(m['mood'] for m in recent_moods)
        
        return {
            'average_mood': statistics.mean(scores),
            'mood_variance': statistics.variance(scores) if len(scores) > 1 else 0,
            'dominant_mood': mood_counts.most_common(1)[0][0],
            'mood_distribution': dict(mood_counts)
        }

    def get_recommendations(self) -> Dict:
        """Get music recommendations based on recent mood trends"""
        trends = self.get_mood_trends()
        if 'error' in trends:
            return {'error': 'Insufficient data for recommendations'}
            
        dominant_mood = trends['dominant_mood']
        recommended_genres = self.analyzer.genre_mapping.get(dominant_mood, [])
        
        return {
            'mood_analysis': trends,
            'recommended_genres': recommended_genres,
            'recommendation_basis': f'Based on your dominant mood: {dominant_mood}'
        }

    def get_mood_history(self, limit: int = 10) -> List[Dict]:
        """Retrieve recent mood entries"""
        return sorted(
            self.moods_db,
            key=lambda x: x['timestamp'],
            reverse=True
        )[:limit]
