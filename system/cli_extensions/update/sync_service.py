import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class SyncHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            os.system('git add . && git commit -m "Auto-sync" && git push')

if __name__ == "__main__":
    path = os.getcwd()
    event_handler = SyncHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()