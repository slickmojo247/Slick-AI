# upgrade_scripts/2.2.x-2.3.x.py
class UpgradeScript:
    def apply_to(self, file_path):
        try:
            with open(file_path) as f:
                content = f.read()
                
            # Example upgrade: Add new config fields
            if "config.py" in str(file_path):
                new_content = content.replace(
                    "DEFAULT_CONFIG = {",
                    "DEFAULT_CONFIG = {\n    'delta_upgrades': True,"
                )
                with open(file_path, 'w') as f:
                    f.write(new_content)
                return True
                    
        except Exception as e:
            print(f"Upgrade failed for {file_path}: {str(e)}")
            return False