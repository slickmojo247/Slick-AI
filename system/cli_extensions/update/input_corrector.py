# knowledge/input_corrector.py
import re
from .core import KnowledgeCore

class InputCorrector:
    def __init__(self):
        self.knowledge = KnowledgeCore()
        self.common_patterns = [
            (r',(\s*[\)\]\}])', r'\1'),  # Trailing commas before closing brackets
            (r',(\s*;)', r'\1'),         # Commas before semicolons
            (r'(\w)\s*,\s*(\w)', r'\1, \2'),  # Missing space after comma
            (r'\.(\w)', r'. \1'),        # Missing space after period
            (r'(\W)\.(\w)', r'\1. \2'),  # Missing space after period (with prefix)
            (r';(\w)', r'; \1'),         # Missing space after semicolon
        ]
    
    def correct_common_patterns(self, text):
        """Fix common punctuation mistakes using regex patterns"""
        corrected = text
        for pattern, replacement in self.common_patterns:
            corrected = re.sub(pattern, replacement, corrected)
        return corrected
    
    def correct_using_knowledge(self, text, context=None):
        """Fix mistakes using the common mistakes database"""
        suggestions = self.knowledge.suggest_corrections(text, context)
        if suggestions:
            # Use the first suggestion that changes the text
            for suggestion in suggestions:
                if suggestion['corrected'] != text:
                    return suggestion['corrected']
        return text
    
    def correct_input(self, text, context=None):
        """Apply all correction layers"""
        # Step 1: Correct common punctuation patterns
        corrected = self.correct_common_patterns(text)
        
        # Step 2: Correct using knowledge base
        corrected = self.correct_using_knowledge(corrected, context)
        
        return corrected
    
    def learn_from_correction(self, original, corrected, context=None):
        """Add a new mistake-correction pair to the database"""
        if original != corrected:
            self.knowledge.add_mistake_correction(original, corrected, context)