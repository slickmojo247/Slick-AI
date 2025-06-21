# AI Preferences Loader
import csv

def load_ai_preferences():
    with open('slick/data/ai_preferences_details.csv') as f:
        reader = csv.DictReader(f)
        for row in reader:
            return {
                'tone': row['tone'],
                'humor_level': row['humor_level'],
                'proactiveness': row['proactiveness'],
                'feedback_frequency': row['feedback_frequency'],
                'memory_decay_alpha': float(row['memory_decay_alpha']),
                'memory_decay_beta': float(row['memory_decay_beta']),
                'memory_decay_gamma': float(row['memory_decay_gamma']),
                'contextual_recall_weights': eval(row['contextual_recall_weights'])
            }