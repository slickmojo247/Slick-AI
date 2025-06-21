# Interest-Based Enhancement
from slick.config import load_ai_profile

profile = load_ai_profile()

class InterestEnhancer:
    def enhance(self, content):
        # Boost relevance for profile interests
        for interest in profile['interests']:
            if interest.lower() in content.lower():
                return f"
                ⭐ SPECIAL INTEREST DETECTED ({interest}) ⭐
                {content}
                [Additional context loaded]
                "
        return content