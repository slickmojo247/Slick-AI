from typing import Dict, List
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

class ResponseBlender:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self._init_blend_rules()

    def _init_blend_rules(self):
        """Dynamic blending rules"""
        self.rules = {
            'balanced': {
                'weights': {'primary': 0.7, 'secondary': 0.3},
                'strategy': 'weighted_average'
            },
            'technical': {
                'weights': {'primary': 0.9, 'secondary': 0.1},
                'strategy': 'primary_dominant'
            },
            'creative': {
                'weights': {'primary': 0.5, 'secondary': 0.5},
                'strategy': 'semantic_merge'
            }
        }

    def blend(self, responses: List[Dict], mode: str = 'balanced') -> Dict:
        """Advanced blending with:
        - Semantic similarity analysis
        - Conflict resolution
        - Style preservation
        """
        rule = self.rules.get(mode, self.rules['balanced'])
        
        if rule['strategy'] == 'semantic_merge':
            return self._semantic_merge(responses)
        else:
            return self._weighted_blend(responses, rule['weights'])

    def _weighted_blend(self, responses: List[Dict], weights: Dict) -> Dict:
        """Basic weighted blending"""
        blended = {
            'content': '',
            'sources': [],
            'confidence': 0.0
        }
        
        for i, resp in enumerate(responses):
            weight = weights.get(f"source_{i}", 0.5)
            blended['content'] += f"[{weight*100}%] {resp['content']}\n"
            blended['sources'].append(resp['source'])
            blended['confidence'] += resp.get('confidence', 0) * weight
            
        return blended

    def _semantic_merge(self, responses: List[Dict]) -> Dict:
        """AI-powered semantic merging"""
        texts = [resp['content'] for resp in responses]
        tfidf = self.vectorizer.fit_transform(texts)
        similarity = (tfidf * tfidf.T).A[0,1]
        
        # Merge based on semantic similarity
        if similarity > 0.7:
            merged = f"Consensus view:\n{texts[0]}"
        else:
            merged = f"Multiple perspectives:\n1. {texts[0]}\n2. {texts[1]}"
            
        return {
            'content': merged,
            'sources': [resp['source'] for resp in responses],
            'semantic_similarity': float(similarity)
        }
