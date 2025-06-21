# Memory System Integration
from slick.config import load_ai_profile
from .memory_core import MemoryBank

profile = load_ai_profile()
MEMORY_BANK = MemoryBank()

def apply_memory_bias():
    # Apply cognitive preferences from profile
    if profile['cognitive_preferences']['memory_bias'] == 'recent':
        MEMORY_BANK.decay_alpha *= 0.8  # Less decay for recent bias
    elif profile['cognitive_preferences']['memory_bias'] == 'important':
        MEMORY_BANK.decay_beta *= 0.7  # Preserve important memories longer

def initialize_memory():
    # Load from CSV
    try:
        import csv
        with open('slick/data/memory_nodes.csv') as f:
            reader = csv.DictReader(f)
            for row in reader:
                MEMORY_BANK.add_memory(
                    event_id=row['event_id'],
                    sensory_context=eval(row['sensory_context']),
                    importance=float(row['emotional_weight']),
                    category='preload'
                )
        return f"Loaded {len(MEMORY_BANK.long_term)} initial memories"
    except Exception as e:
        return f"Memory initialization error: {str(e)}"