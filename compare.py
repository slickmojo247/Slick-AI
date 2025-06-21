import pandas as pd
import glob

# Load all CSV reports
reports = {}
for csv_file in glob.glob("update/*.csv"):
    df = pd.read_csv(csv_file)
    reports[csv_file] = df

# Compare with current files
with open("current_files.txt") as f:
    current_files = set(f.read().splitlines())

action_plan = {
    "create": [],
    "update": [], 
    "merge": [],
    "delete": []
}

for report, df in reports.items():
    for _, row in df.iterrows():
        file_path = row.get('File') or row.get('Path') or f"{row.get('Directory','')}/{row.get('File','')}"
        if pd.notna(file_path):
            if file_path not in current_files:
                if "Create" in str(row.get('Action')) or "New" in str(row.get('Status')):
                    action_plan["create"].append(file_path)
            elif "Update" in str(row.get('Action')):
                action_plan["update"].append(file_path)
            elif "Merge" in str(row.get('Action')):
                action_plan["merge"].append(file_path)
            elif "Delete" in str(row.get('Action')):
                action_plan["delete"].append(file_path)

print("Action Plan:")
for action, files in action_plan.items():
    print(f"\n{action.upper()} ({len(files)} files):")
    for f in sorted(files)[:5]:  # Show first 5 examples
        print(f"  - {f}")
    if len(files) > 5: print(f"  ... and {len(files)-5} more")