# utils/event_bus.py
from collections import defaultdict
import logging
from typing import Callable, Any

class EventBus:
    def __init__(self):
        self.listeners = defaultdict(list)
        self.history = []

    def subscribe(self, event_name: str, callback: Callable):
        self.listeners[event_name].append(callback)

    def unsubscribe(self, event_name: str, callback: Callable):
        if callback in self.listeners[event_name]:
            self.listeners[event_name].remove(callback)

    def emit(self, event_name: str, payload: Any = None):
        self.history.append((event_name, payload))
        for callback in self.listeners[event_name]:
            try:
                callback(payload)
            except Exception as e:
                logging.error(f"EventBus error in {event_name}: {str(e)}")