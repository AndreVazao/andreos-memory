import os
import time
import subprocess
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

MEMORY_PATH = os.getenv("ANDREOS_MEMORY", r"C:\ProgramasGodmode\andreos-memory")
DEBOUNCE_SECONDS = 5

class MemoryChangeHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_commit_time = 0

    def on_any_event(self, event):
        if event.is_directory:
            return
        self.try_commit()

    def try_commit(self):
        now = time.time()
        if now - self.last_commit_time < DEBOUNCE_SECONDS:
            return
        self.last_commit_time = now
        self.commit_changes()

    def commit_changes(self):
        try:
            print("[MEMORY SYNC] Change detected, syncing...")
            
            subprocess.run(["git", "-C", MEMORY_PATH, "add", "."], check=False)
            
            timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
            commit_msg = f"memory-sync: auto snapshot {timestamp}"
            
            subprocess.run(["git", "-C", MEMORY_PATH, "commit", "-m", commit_msg], check=False)
            subprocess.run(["git", "-C", MEMORY_PATH, "push"], check=False)
            
            print("[MEMORY SYNC] Commit completed")
        except Exception as e:
            print(f"[MEMORY SYNC ERROR] {e}")

def ensure_git_repo():
    if not os.path.exists(os.path.join(MEMORY_PATH, ".git")):
        print("[INIT] Initializing git repository...")
        subprocess.run(["git", "-C", MEMORY_PATH, "init"], check=False)
        subprocess.run(["git", "-C", MEMORY_PATH, "branch", "-M", "main"], check=False)

if __name__ == "__main__":
    print(f"[MEMORY SYNC] Starting daemon on: {MEMORY_PATH}")
    ensure_git_repo()

    event_handler = MemoryChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, MEMORY_PATH, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()