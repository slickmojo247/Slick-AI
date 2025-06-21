import logging
import numpy as np
from typing import Dict, Any, List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

class LearningEngine:
    def __init__(self, n_clusters: int = 5):
        self.log = logging.getLogger(__name__)
        self.vectorizer = TfidfVectorizer(max_features=1000)
        self.clusterer = KMeans(n_clusters=n_clusters)
        self.feedback_history = []
        self.log.info("Learning Engine initialized")

    def process_feedback(self, feedback: Dict[str, Any]):
        """Store and learn from user feedback"""
        self.feedback_history.append(feedback)
        
        if len(self.feedback_history) > 10:  # Minimum batch size
            self._update_models()

    def _update_models(self):
        """Update ML models with new feedback"""
        texts = [fb['query'] + " " + fb['comment'] for fb in self.feedback_history]
        
        try:
            X = self.vectorizer.fit_transform(texts)
            self.clusterer.fit(X)
            self.log.info("Updated learning models")
        except Exception as e:
            self.log.error(f"Model update failed: {e}")

    def suggest_improvements(self, query: str) -> List[str]:
        """Suggest response improvements based on learned patterns"""
        try:
            vec = self.vectorizer.transform([query])
            cluster = self.clusterer.predict(vec)[0]
            
            similar_feedback = [
                fb for i, fb in enumerate(self.feedback_history)
                if self.clusterer.labels_[i] == cluster
            ]
            
            return list(set(
                fb['suggestion'] for fb in similar_feedback
                if 'suggestion' in fb
            ))[:3]
        except Exception as e:
            self.log.error(f"Suggestion failed: {e}")
            return []
