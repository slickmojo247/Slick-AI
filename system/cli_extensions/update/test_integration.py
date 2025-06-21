# test_integration.py
class TestSlickSystem(unittest.TestCase):
    def test_full_flow(self):
        # Simulate VSCode input
        vscode_input = "How to connect to DeepSeek?"
        controller = SlickController()
        
        # Process through all layers
        response = controller.route_request(
            source="vscode",
            input_data=vscode_input
        )
        
        # Verify knowledge integration
        self.assertIn("DeepSeek API", response)
        self.assertTrue(controller.knowledge.has_recent_interaction())

    def wsl_to_win_path(wsl_path):
    """Convert /mnt/c/Users/ to C:/Users/"""
    if wsl_path.startswith('/mnt/'):
        drive = wsl_path[5].upper() + ':'
        return drive + wsl_path[6:].replace('/', '\\')
    return wsl_path

class EventBus:
    _subscriptions = defaultdict(list)
    
    @classmethod
    def publish(cls, event_type, data):
        for callback in cls._subscriptions[event_type]:
            callback(data)
    
    @classmethod
    def subscribe(cls, event_type, callback):
        cls._subscriptions[event_type].append(callback)