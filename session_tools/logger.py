
def export_to_csv(self, session_data):
    """Appends session data to CSV per your blueprint"""
    import csv
    from datetime import datetime
    with open("sessions/session_log.csv", "a") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now(),
            session_data["prompt"],
            session_data["response"],
            session_data.get("tags", "")
        ])
