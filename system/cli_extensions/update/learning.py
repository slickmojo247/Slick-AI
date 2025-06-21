# knowledge/learning.py
from .core import KnowledgeCore
import random

class LearningModule:
    def __init__(self, user_id):
        self.knowledge = KnowledgeCore()
        self.user_id = user_id
        self.learning_paths = {
            "beginner": ["Variables", "Data Types", "Control Structures"],
            "intermediate": ["Functions", "Classes", "Error Handling"],
            "advanced": ["Decorators", "Generators", "Metaclasses"]
        }
    
    def get_learning_path(self, level="beginner"):
        """Get a structured learning path for the user"""
        path = self.learning_paths.get(level, self.learning_paths["beginner"])
        return {
            "level": level,
            "path": path,
            "progress": self.get_user_progress(level)
        }
    
    def get_user_progress(self, level):
        """Get user's progress on a learning path"""
        # In a real implementation, this would come from a database
        return {topic: random.randint(0, 100) for topic in self.learning_paths[level]}
    
    def get_learning_content(self, topic):
        """Get encyclopedia and coding manual content for a topic"""
        encyclopedia = self.knowledge.search_encyclopedia(topic, max_results=1)
        coding_manual = self.knowledge.search_coding_manual("Python", topic)
        
        return {
            "encyclopedia": dict(encyclopedia[0]) if encyclopedia else None,
            "coding_manual": dict(coding_manual) if coding_manual else None
        }
    
    def generate_quiz(self, topic, difficulty="easy"):
        """Generate a quiz on a specific topic"""
        # In a real implementation, this would come from a question bank
        questions = [
            {
                "question": "What is a variable?",
                "options": [
                    "A container for storing data values",
                    "A type of loop",
                    "A function definition",
                    "An error handling mechanism"
                ],
                "answer": 0
            },
            {
                "question": "How do you define a variable in Python?",
                "options": [
                    "var x = 5",
                    "x := 5",
                    "x = 5",
                    "variable x = 5"
                ],
                "answer": 2
            }
        ]
        
        return {
            "topic": topic,
            "difficulty": difficulty,
            "questions": questions
        }