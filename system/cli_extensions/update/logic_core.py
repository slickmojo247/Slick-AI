from slick.config import load_ai_profile, load_ai_preferences
from slick.memory import MEMORY_BANK
from slick.personality import PersonalityEngine
from slick.cognitive import LearningAdapter, InterestEnhancer

profile = load_ai_profile()
prefs = load_ai_preferences()

class SlickLogicEngine:
    def __init__(self, personality_mode="standard"):
        self.state = {}
        self.personality = PersonalityEngine()
        self.learning_adapter = LearningAdapter()
        self.interest_enhancer = InterestEnhancer()
        self.interests = profile['interests']
        self.personality_mode = personality_mode  # "standard" or "homer"

    def handle_command(self, command, context=None):
        # Apply memory and personality
        context = context or {}
        memory_context = MEMORY_BANK.contextual_recall(command, context)
        
        # Handle Homer mode first
        if self.personality_mode == "homer":
            return self._handle_homer_mode(command)
            
        # Standard AI processing
        # Interest-based prioritization
        if any(interest in command for interest in self.interests):
            command = f"PRIORITY: {command}"

        # Personality-based processing
        if 'joke' in command and prefs['humor_level'] != 'none':
            response = "Why don't scientists trust atoms? Because they make up everything!"
        elif 'analyze' in command and profile['personality_traits']['analytical'] > 0.7:   
            response = "Running deep analysis with quantum simulation..."
        else:
            response = f"Processing: {command} with context: {memory_context[:1]}"

        # Apply learning style and interest enhancement
        response = self.learning_adapter.adapt_content(response)
        response = self.interest_enhancer.enhance(response)

        return self.personality.generate_response_style(response)

    def _handle_homer_mode(self, command):
        command = command.strip().lower()
        # Homer-style responses
        if "donut" in command or "doughnut" in command:
            return "Mmm... donuts... is there anything they can't do?"
        if "beer" in command:
            return "Mmm... beer..."
        if "work" in command:
            return "D'oh! Why'd you have to bring that up?"
        if "name is" in command:
            name = command.split("is")[-1].strip().capitalize()
            MEMORY_BANK.add_memory(f"User name is {name}", category="user")
            return f"Nice to meet you, {name}! Got any donuts?"
        if "who am i" in command:
            memories = MEMORY_BANK.contextual_recall("User name")
            if memories:
                return f"You told me you were {memories[0]['content'].split('is')[-1].strip()}"
            return "I don't think you've told me your name yet. D'oh!"
        
        return f"Processing: {command}... Woo-hoo!"