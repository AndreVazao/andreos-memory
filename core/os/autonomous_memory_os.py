import os
import time
import json
import queue
import threading
import subprocess
from datetime import datetime

from core.injector.memory_context_injector import injector
from core.agents.agent_runtime import AgentRuntime
from core.router.memory_router import router

MEMORY_PATH = os.getenv("ANDREOS_MEMORY", r"C:\ProgramasGodmode\andreos-memory")

# -----------------------------
# TASK QUEUE (PERSISTENCE LIGHT)
# -----------------------------

class TaskQueue:
    def __init__(self):
        self.q = queue.Queue()
        self.history = []

    def add(self, task: str, meta: dict = None):
        payload = {
            "task": task,
            "meta": meta or {},
            "timestamp": datetime.utcnow().isoformat()
        }
        self.q.put(payload)

    def get(self):
        return self.q.get()

    def size(self):
        return self.q.qsize()


# -----------------------------
# TOOL EXECUTION ENGINE
# -----------------------------

class ToolExecutor:
    def run_shell(self, command: str) -> dict:
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return {
                "command": command,
                "stdout": result.stdout[-2000:],
                "stderr": result.stderr[-2000:],
                "code": result.returncode
            }
        except Exception as e:
            return {"error": str(e), "command": command}

    def run_git(self, args: str) -> dict:
        cmd = f"git -C {MEMORY_PATH} {args}"
        return self.run_shell(cmd)


# -----------------------------
# MEMORY WRITE LOOP
# -----------------------------

class MemoryWriter:
    def write_event(self, event: dict):
        try:
            path = os.path.join(MEMORY_PATH, "core", "events.log")
            os.makedirs(os.path.dirname(path), exist_ok=True)

            with open(path, "a", encoding="utf-8") as f:
                f.write(json.dumps(event) + "\n")
        except Exception as e:
            print(f"[MEMORY WRITER ERROR] {e}")


# -----------------------------
# AUTONOMOUS OS
# -----------------------------

class AutonomousMemoryOS:
    """
    FINAL LAYER:
    Autonomous memory-driven agent operating system.
    """

    def __init__(self):
        self.queue = TaskQueue()
        self.executor = ToolExecutor()
        self.writer = MemoryWriter()
        self.agents = AgentRuntime()
        self.running = False

    def submit_task(self, task: str, meta: dict = None):
        self.queue.add(task, meta)

    def process_task(self, task_obj: dict):
        task = task_obj["task"]

        # 1. Inject memory
        context = injector.inject(task)

        # 2. Agent execution
        result = self.agents.execute(task)

        # 3. Write memory event
        event = {
            "task": task,
            "context_size": len(context.get("context", "")),
            "result_summary": result.get("review", {}),
            "timestamp": datetime.utcnow().isoformat()
        }

        self.writer.write_event(event)

        # 4. Optional autonomous git sync (lightweight)
        try:
            self.executor.run_git("add .")
            self.executor.run_git(f'commit -m "auto-os: {task[:50]}"')
        except:
            pass

        return result

    def loop(self):
        self.running = True
        print("[AUTONOMOUS OS] Starting main loop...")

        while self.running:
            try:
                if self.queue.size() == 0:
                    time.sleep(1)
                    continue

                task_obj = self.queue.get()

                print(f"[AUTONOMOUS OS] Processing: {task_obj['task']}")

                result = self.process_task(task_obj)

                print("[AUTONOMOUS OS] Done task")

            except Exception as e:
                print(f"[AUTONOMOUS OS ERROR] {e}")

    def stop(self):
        self.running = False


# Global instance
os_runtime = AutonomousMemoryOS()


if __name__ == "__main__":
    os_runtime.submit_task("initialize autonomous memory system")

    thread = threading.Thread(target=os_runtime.loop, daemon=True)
    thread.start()

    time.sleep(5)
    os_runtime.stop()
