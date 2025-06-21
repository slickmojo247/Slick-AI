# AI Profile Loader
import json
import csv

def load_ai_profile():
    # Load from JSON snapshot
    try:
        with open('slick/data/snapshot_config.json') as f:
            config = json.load(f)
            return config['ai_profile']
    except:
        # Fallback to CSV if JSON unavailable
        return load_ai_profile_csv()

def load_ai_profile_csv():
    with open('slick/data/profile_details.csv') as f:
        reader = csv.DictReader(f)
        for row in reader:
            return {
                'name': row['name'],
                'cognitive_preferences': {
                    'learning_style': row['cognitive_preferences_learning_style'],
                    'memory_bias': row['cognitive_preferences_memory_bias']
                },
                'personality_traits': {
                    'curiosity': float(row['personality_traits_curiosity']),
                    'analytical': float(row['personality_traits_analytical'])
                },
                'interests': row['interests'].split(';'),
                'habits': row['habits'].split(';'),
                'health_metrics': {
                    'sleep_avg': float(row['health_metrics_sleep_avg'])
                },
                'privacy_settings': {
                    'data_retention': row['privacy_settings_data_retention'],
                    'share_anonymous_data': row['privacy_settings_share_anonymous_data'].lower() == 'true'
                }
            }