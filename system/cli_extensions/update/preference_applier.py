# Preference Applier
from slick.config import load_ai_preferences

prefs = load_ai_preferences()

class PreferenceApplier:
    def apply(self, content):
        # Apply tone preferences
        if prefs['tone'] == 'professional_but_friendly':
            content = content.replace("I think", "My analysis suggests")
            content = content.replace("can't", "cannot")
        
        # Apply humor level
        if prefs['humor_level'] == 'low':
            content = content.split('🤖')[0] if '🤖' in content else content
        elif prefs['humor_level'] == 'high':
            if not any(emoji in content for emoji in ['🤖', '✨', '⭐']):
                content += " 😊"
                
        return content