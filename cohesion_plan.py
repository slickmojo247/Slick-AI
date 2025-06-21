import pandas as pd
from pathlib import Path

class ProjectAnalyzer:
    def __init__(self, update_dir="update"):
        self.blueprints = {}
        for csv in Path(update_dir).glob('*.csv'):
            try: 
                self.blueprints[csv.stem] = pd.read_csv(csv)
            except:
                continue
        self.current_files = {str(p) for p in Path('.').rglob('*') if p.is_file() and ':memory:' not in str(p)}

    def generate_plan(self):
        plan = {'create':[], 'update':[], 'merge':[]}
        for df in self.blueprints.values():
            for _, row in df.iterrows():
                path = row.get('File') or f"{row.get('Directory','')}/{row.get('File','')}"
                if not path or not isinstance(path, str): 
                    continue
                if path not in self.current_files and ('Create' in str(row.get('Action',''))):
                    plan['create'].append(path)
                elif 'Update' in str(row.get('Action','')):
                    plan['update'].append(path)
                elif 'Merge' in str(row.get('Action','')):
                    plan['merge'].append(path)
        return plan

if __name__ == "__main__":
    plan = ProjectAnalyzer().generate_plan()
    for action, files in plan.items():
        print(f"\n{action.upper()} ({len(files)} files):")
        for f in sorted(files)[:5]:
            print(f"  - {f}")
        if len(files) > 5:
            print(f"  ... and {len(files)-5} more")
