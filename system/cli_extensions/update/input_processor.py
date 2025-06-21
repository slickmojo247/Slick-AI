import enchant
from nltk.corpus import wordnet
import re

class InputProcessor:
    def __init__(self, knowledge_base):
        self.knowledge_base = knowledge_base
        self.spell_checker = enchant.Dict("en_US")
        self.common_mistakes = {
            "teh": "the",
            "adn": "and",
            "thsi": "this",
            "fucntion": "function"
        }
    
    def correct(self, text):
        """Correct spelling and common mistakes"""
        # Fix common mistakes
        for mistake, correction in self.common_mistakes.items():
            text = re.sub(rf'\b{mistake}\b', correction, text)
        
        # Spell check
        words = text.split()
        corrected = []
        for word in words:
            if not self.spell_checker.check(word):
                suggestions = self.spell_checker.suggest(word)
                if suggestions:
                    corrected.append(suggestions[0])
                else:
                    corrected.append(word)
            else:
                corrected.append(word)
        return " ".join(corrected)
    
    def enhance(self, text):
        """Enhance input with knowledge base"""
        # Extract keywords
        keywords = set(word for word in text.split() if len(word) > 3)
        
        # Find related knowledge
        related = []
        for keyword in keywords:
            results = self.knowledge_base.query(keyword)
            if results:
                related.extend(results)
        
        # Add context if found
        if related:
            context = "\nRelated knowledge:\n" + "\n".join(
                f"- {item['title']}: {item['excerpt']}" 
                for item in related[:3]
            )
            return text + context
        
        return text
    
    def learn(self, input_text, response):
        """Learn from interactions"""
        # Extract key concepts
        concepts = [word for word in input_text.split() if len(word) > 4]
        
        # Create or update session
        for concept in concepts:
            session_id = f"auto_{concept.lower()}"
            existing = self.knowledge_base.sessions.get(session_id, {})
            new_content = existing.get('content', '') + f"\n\n{datetime.now()}\nQ: {input_text}\nA: {response}"
            
            self.knowledge_base.add_session(
                session_id,
                f"Auto: {concept}",
                new_content
            )