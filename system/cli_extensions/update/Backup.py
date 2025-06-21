import csv
import os
import datetime
import json

import logging
from typing import List, Dict, Any, Optional 

# Attempt to import UserProfile, AIResponsePreferences, and MemoryNode
# These are expected to be defined in memory_node.py or a shared models.py
try:
    from memory_node import UserProfile, AIResponsePreferences, MemoryNode
except ImportError:
    # Define placeholder classes if the import fails.
    # This allows SaveSystem to be defined, but it won't function correctly
    # without the actual class definitions.
    class UserProfile: pass
    class AIResponsePreferences: pass
    class MemoryNode: pass
    print("Warning: Could not import UserProfile, AIResponsePreferences, or MemoryNode. Backup functionality will be limited.")


class SaveSystem:
    def __init__(self, save_directory: str):
        # os.makedirs(save_directory, exist_ok=True) # Redundant, done below
        self.save_directory = os.path.abspath(save_directory)
        os.makedirs(self.save_directory, exist_ok=True)

        # Setup logging
        self.logs_directory = os.path.join(os.path.dirname(self.save_directory), "logs")
        os.makedirs(self.logs_directory, exist_ok=True)
        
        log_file_path = os.path.join(self.logs_directory, "backup.log")
        
        self.logger = logging.getLogger("BackupSystem")
        if not self.logger.handlers: # Avoid adding multiple handlers if class is instantiated multiple times
            self.logger.setLevel(logging.INFO)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            
            file_handler = logging.FileHandler(log_file_path)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
            
            # Optional: Add a stream handler to also print logs to console
            # stream_handler = logging.StreamHandler()
            # stream_handler.setFormatter(formatter)
            # self.logger.addHandler(stream_handler)
 
    def _generate_timestamp_id(self) -> str:
        """Generates a unique ID based on the current timestamp."""
        return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
 
    def save_profile(self, user_profile: UserProfile, ai_preferences: AIResponsePreferences, file_name: str = "user_profile.json"):
        profile_data = {
            "user_profile": user_profile.to_dict(),
            "ai_preferences": ai_preferences.to_dict()
        }

        with open(os.path.join(self.save_directory, file_name), "w") as file:
            json.dump(profile_data, file, indent=4)
        self.logger.info(f"Profile saved to {os.path.join(self.save_directory, file_name)}")
 
    def load_profile(self, file_name: str = "user_profile.json"):
        try:
            with open(os.path.join(self.save_directory, file_name), "r") as file:
                profile_data = json.load(file)
                user_profile_data = profile_data["user_profile"]
                ai_preferences_data = profile_data["ai_preferences"]
                user_profile = UserProfile(**user_profile_data) # type: ignore
                ai_preferences = AIResponsePreferences(**ai_preferences_data) # type: ignore
                return user_profile, ai_preferences
        except FileNotFoundError:
            return None, None
 
    def backup_to_csvs(self, profiles: List[UserProfile], 
                       preferences: List[AIResponsePreferences], 
                       memory_nodes: List[MemoryNode], 
                       save_directory_override: Optional[str] = None):
        current_save_dir = save_directory_override if save_directory_override else self.save_directory
        is_full_backup_context = bool(save_directory_override)

        # Backup UserProfiles
        if profiles:
            profile_filename = "profile_details.csv" if is_full_backup_context else "profiles.csv"
            profile_path = os.path.join(current_save_dir, profile_filename)
            with open(profile_path, "w", newline="", encoding="utf-8") as f:
                if profiles: # Ensure profiles list is not empty
                    sample_dict = profiles[0].to_dict()
                    fieldnames = []
                    for key, value in sample_dict.items():
                        if isinstance(value, dict):
                            for sub_key in value.keys():
                                fieldnames.append(f"{key}_{sub_key}")
                        elif isinstance(value, list):
                            fieldnames.append(key) 
                        else:
                            fieldnames.append(key)
                    
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    for profile in profiles:
                        row_data = {}
                        profile_dict = profile.to_dict()
                        for key, value in profile_dict.items():
                            if isinstance(value, dict):
                                for sub_key, sub_value in value.items():
                                    row_data[f"{key}_{sub_key}"] = sub_value
                            elif isinstance(value, list):
                                row_data[key] = ";".join(map(str,value))
                            else:
                                row_data[key] = value
                        writer.writerow(row_data)
            self.logger.info(f"Profiles backed up to {profile_path}")

        # Backup AIResponsePreferences
        if preferences:
            preferences_filename = "ai_preferences_details.csv" if is_full_backup_context else "ai_preferences.csv"
            preferences_path = os.path.join(current_save_dir, preferences_filename)
            with open(preferences_path, "w", newline="", encoding="utf-8") as f:
                if preferences: # Ensure preferences list is not empty
                    sample_dict = preferences[0].to_dict()
                    fieldnames = [key for key in sample_dict.keys()] # Assumes flat dict or list values handled by to_dict
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    for pref in preferences:
                        writer.writerow(pref.to_dict())
            self.logger.info(f"AI Preferences backed up to {preferences_path}")

        # Backup MemoryNodes - only if not in full backup context (handled separately in create_full_backup)
        # or if explicitly passed to this function outside of create_full_backup
        if memory_nodes and not is_full_backup_context:
            memory_nodes_path = os.path.join(current_save_dir, "memory_nodes.csv")
            # Define fieldnames based on MemoryNode attributes
            # Ensure these attributes exist on your MemoryNode objects
            fieldnames = ["event_id", "timestamp", "sensory_context", 
                          "emotional_weight", "embeddings_type"]
            if memory_nodes and hasattr(memory_nodes[0], 'metadata'): # Check if list not empty first
                # This assumes all nodes have 'metadata' if the first one does.
                # A more robust check might iterate or ensure consistent structure.
                if 'metadata' not in fieldnames: # Avoid duplicate
                    fieldnames.append("metadata")

            with open(memory_nodes_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for node in memory_nodes:
                    node_data = {
                        "event_id": node.event_id, # type: ignore
                        "timestamp": node.timestamp, # type: ignore
                        "sensory_context": json.dumps(node.sensory_context), # type: ignore
                        "emotional_weight": node.emotional_weight, # type: ignore
                        "embeddings_type": type(node.embeddings).__name__, # type: ignore
                    }
                    if 'metadata' in fieldnames and hasattr(node, 'metadata'):
                        node_data["metadata"] = json.dumps(node.metadata) # type: ignore
                    writer.writerow(node_data)
            self.logger.info(f"Memory Nodes backed up to {memory_nodes_path}")
 
    def create_full_backup(self, ai_profile: UserProfile, 
                           ai_preferences: AIResponsePreferences, 
                           memory_nodes: List[MemoryNode]) -> str:
        self.logger.info("Starting full backup process...")
        backup_id = self._generate_timestamp_id()
        backup_subdir = os.path.join(self.save_directory, backup_id)
        os.makedirs(backup_subdir, exist_ok=True)

        snapshot_config_data = {
            "ai_profile": ai_profile.to_dict(),
            "ai_preferences": ai_preferences.to_dict()
        }
        json_config_path = os.path.join(backup_subdir, "snapshot_config.json")
        with open(json_config_path, "w") as file:
            json.dump(snapshot_config_data, file, indent=4)
        self.logger.info(f"AI snapshot config saved to {json_config_path}")
 
        if memory_nodes:
            memory_nodes_csv_path = os.path.join(backup_subdir, "memory_nodes.csv")
            fieldnames = ["event_id", "timestamp", "sensory_context", "emotional_weight", "embeddings_type"]
            with open(memory_nodes_csv_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for node in memory_nodes:
                    writer.writerow({
                        "event_id": node.event_id, # type: ignore
                        "timestamp": node.timestamp, # type: ignore
                        "sensory_context": json.dumps(node.sensory_context), # type: ignore
                        "emotional_weight": node.emotional_weight, # type: ignore
                        "embeddings_type": type(node.embeddings).__name__ # type: ignore
                    })
            self.logger.info(f"Memory Nodes CSV saved to {memory_nodes_csv_path}")
         
        # Simplified CSV backup for profile and preferences in the timestamped folder
        # Create CSV backups for profile and preferences within the timestamped backup subfolder
        self.backup_to_csvs([ai_profile], [ai_preferences], [], save_directory_override=backup_subdir)

        log_message = f"Full AI state backup created with ID {backup_id} in directory: {backup_subdir}"
        self.logger.info(log_message)
        print(log_message) # Also print to console for immediate feedback
        return backup_subdir
