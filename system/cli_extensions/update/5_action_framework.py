# Merges: action_base.py, action_game.py
class Action:
    registry = []
    
    @classmethod
    def register(cls, pattern):
        def decorator(fn):
            cls.registry.append((re.compile(pattern), fn))
            return fn
        return decorator

@Action.register(r"trigger (\w+)")
def handle_event(match):
    return f"Event {match.group(1)} triggered!"

def execute_action(text):
    for pattern, handler in Action.registry:
        if match := pattern.match(text):
            return handler(match)